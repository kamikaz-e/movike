package dev.kamikaze.movike.presentation.ui.fragments

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.viewModels
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.paging.CombinedLoadStates
import androidx.paging.LoadState
import dev.kamikaze.movike.presentation.adapters.LoadingStateAdapter
import dev.kamikaze.movike.common.base.BaseFragment
import dev.kamikaze.movike.presentation.customviews.search.SearchCallback
import dev.kamikaze.movike.databinding.FragmentSearchBinding
import dev.kamikaze.movike.presentation.navigation.navigators.SearchNavigator
import dev.kamikaze.movike.presentation.ui.viewmodel.SearchViewModel
import dev.kamikaze.movike.presentation.adapters.SearchMovieAdapter
import dev.kamikaze.movike.presentation.adapters.callbacks.SearchMovieItemClickListener
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import javax.inject.Inject

class SearchFragment : BaseFragment<SearchNavigator>(),
    SearchMovieItemClickListener, SearchCallback {

    @Inject
    lateinit var factory: ViewModelProvider.Factory
    private val viewModel: SearchViewModel by viewModels { factory }

    private var _binding: FragmentSearchBinding? = null
    private val binding: FragmentSearchBinding get() = _binding!!

    @Inject
    lateinit var adapter: SearchMovieAdapter

    @Inject
    lateinit var loadingStateAdapter: LoadingStateAdapter

    private var job: Job? = null

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentSearchBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onResume() {
        super.onResume()
        binding.customSearchView.callback = this
    }

    override fun onPause() {
        super.onPause()
        binding.customSearchView.callback = null
    }

    override fun onDestroyView() {
        super.onDestroyView()
        job?.cancel()
        _binding = null
    }

    override fun initView() {
        initAdapter()
    }

    override fun onRetryLoad() {
        initView()
    }

    override fun onMovieClicked(movieId: Int) {
        navigator.goToDetailsMovie(movieId)
    }

    override fun onSearch(searchQuery: String) {
        job?.cancel()
        job = getSearchJob(searchQuery)
    }

    override fun onCloseSearchClicked() {
        navigator.navigateUp()
    }

    private fun initAdapter() {
        with(adapter) {
            callback = this@SearchFragment
            addLoadStateListener { handleLoadState(it) }
            loadingStateAdapter.callback = this@SearchFragment
            binding.movieRV.adapter = withLoadStateFooter(loadingStateAdapter)
            binding.movieRV.setHasFixedSize(true)
        }
        binding.customSearchView
    }

    /* private fun onSuccessLoad(movie: Flow<PagingData<Movie>>) {
         onLoadFinish()
         renderUi(movie)
     }*/

    private fun handleLoadState(state: CombinedLoadStates) {
        when (state.refresh) {
            is LoadState.Loading -> onLoading()
            is LoadState.Error -> showError((state.refresh as LoadState.Error).error)
            else -> onLoadFinish()
        }
    }

    private fun getSearchJob(searchString: String): Job {
        return lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.getMovieFlow(searchString).collectLatest { adapter.submitData(it) }
            }
        }
    }

}