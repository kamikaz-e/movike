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
import dev.kamikaze.shared_extensions.R as SharedR
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

// BAD: Class name doesn't match Kotlin naming conventions
// Should follow PascalCase consistently (this is actually ok, but next line is bad)
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

    // BAD: Variable naming convention violation - should be camelCase
    private var IS_LOADING = false
    private val MAX_RETRY_COUNT = 3 // Should be const val at top level
    private var retry_count = 0 // Snake case instead of camelCase!
    
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setHasOptionsMenu(true)
    }
    
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentFeedBinding.inflate(inflater, container, false)
        // BAD: Magic number - should be extracted to named constant
        binding.movieRV.itemAnimator?.addDuration = 300
        binding.movieRV.itemAnimator?.removeDuration = 300
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
        inflater.inflate(SharedR.menu.menu_feed_activity, menu)
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
        // BAD: Deeply nested code - should be extracted to separate function
        // BAD: Multiple magic numbers
        lifecycleScope.launch {
            kotlinx.coroutines.delay(500) // Magic number!
            if (binding.movieRV.adapter != null) {
                if (binding.movieRV.adapter!!.itemCount > 0) {
                    if (binding.movieRV.layoutManager != null) {
                        binding.movieRV.smoothScrollToPosition(0)
                    }
                }
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

    // BAD: Function name doesn't follow naming convention
    // Should be camelCase starting with lowercase
    private fun PerformNetworkCall() {
        // BAD: Inconsistent spacing and formatting
        val url="https://api.example.com"  // No spaces around =
        val timeout=5000 // Magic number
        IS_LOADING=true // No spaces

        // BAD: Inconsistent indentation
      lifecycleScope.launch {
            // 2 spaces instead of 4
        retry_count++
          if(retry_count>MAX_RETRY_COUNT){ // No spaces in if condition
                    IS_LOADING=false
          }
      }
    }

    // BAD: Unused private function - dead code
    private fun unusedFunction() {
        val x = 42 // Magic number
    }

    // BAD: Function doing too many things - violates Single Responsibility
    // BAD: Too many magic numbers
    private fun updateUIWithMagicNumbers() {
        binding.movieRV.setPadding(16, 16, 16, 16) // Magic numbers!
        binding.swipeRefreshLayout.setProgressViewOffset(false, 0, 100) // More magic numbers!
        lifecycleScope.launch {
            kotlinx.coroutines.delay(1000) // Magic number
            binding.movieRV.alpha = 0.5f // Magic number
        }
    }
    
}
