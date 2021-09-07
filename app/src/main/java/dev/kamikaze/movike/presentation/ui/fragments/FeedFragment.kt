package dev.kamikaze.movike.presentation.ui.fragments

import android.os.Bundle
import android.view.*
import androidx.fragment.app.viewModels
import androidx.lifecycle.Lifecycle.State
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.navigation.fragment.findNavController
import androidx.navigation.ui.onNavDestinationSelected
import androidx.paging.CombinedLoadStates
import androidx.paging.LoadState
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import dev.kamikaze.movike.R
import dev.kamikaze.movike.common.base.BaseFragment
import dev.kamikaze.movike.databinding.FragmentFeedBinding
import dev.kamikaze.movike.presentation.adapters.LoadingStateAdapter
import dev.kamikaze.movike.presentation.adapters.MovieAdapter
import dev.kamikaze.movike.presentation.adapters.callbacks.MovieItemClickListener
import dev.kamikaze.movike.presentation.navigation.navigators.FeedNavigator
import dev.kamikaze.movike.presentation.ui.viewmodel.FeedViewModel
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import javax.inject.Inject

class FeedFragment : BaseFragment<FeedNavigator>(), MovieItemClickListener, SwipeRefreshLayout.OnRefreshListener {
    
    private var _binding: FragmentFeedBinding? = null
    private val binding get() = _binding!!
    
    @Inject
    internal lateinit var factory: ViewModelProvider.Factory
    private val viewModel: FeedViewModel by viewModels { factory }
    
    @Inject
    internal lateinit var moviesAdapter: MovieAdapter
    
    @Inject
    internal lateinit var loadingStateAdapter: LoadingStateAdapter
    
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setHasOptionsMenu(true)
    }
    
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentFeedBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        moviesAdapter.apply {
            callback = null
            removeLoadStateListener { handleLoadState(it) }
        }
        loadingStateAdapter.callback = null
        binding.apply {
            swipeRefreshLayout.callback = null
            movieRV.adapter = null
        }
        _binding = null
    }
    
    override fun onRetryLoad() {
        moviesAdapter.retry()
    }
    
    override fun onRefresh() {
        binding.swipeRefreshLayout.showProgress()
        moviesAdapter.refresh()
    }
    
    override fun onCreateOptionsMenu(menu: Menu, inflater: MenuInflater) {
        inflater.inflate(R.menu.menu_feed_activity, menu)
    }
    
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return item.onNavDestinationSelected(findNavController()) || super.onOptionsItemSelected(item)
    }
    
    override fun initView() {
        initAdapter()
        lifecycleScope.launch {
            repeatOnLifecycle(State.STARTED) {
                viewModel.movieFlow.collectLatest { moviesAdapter.submitData(it) }
            }
        }
    }
    
    override fun onMovieClicked(movieId: Int) {
        navigator.goToDetailsMovie(movieId)
    }
    
    override fun onLoadFinish() {
        super.onLoadFinish()
        binding.swipeRefreshLayout.hideProgress()
    }
    
    private fun onFabClicked() {
        binding.movieRV.smoothScrollToPosition(0)
    }
    
    private fun initAdapter() {
        binding.movieRV.apply {
            setHasFixedSize(true)
            adapter = moviesAdapter.withLoadStateFooter(loadingStateAdapter)
            moviesAdapter.apply {
                callback = this@FeedFragment
                addLoadStateListener { handleLoadState(it) }
            }
        }
        loadingStateAdapter.callback = this
        binding.swipeRefreshLayout.callback = this
    }
    
    private fun handleLoadState(state: CombinedLoadStates) {
        when (state.refresh) {
            is LoadState.Loading -> onLoading()
            is LoadState.Error -> showError((state.refresh as LoadState.Error).error)
            is LoadState.NotLoading -> onLoadFinish()
        }
    }
    
}
