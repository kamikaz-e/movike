package dev.kamikaze.movike.presentation.ui.fragments

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import androidx.core.view.isVisible
import androidx.fragment.app.viewModels
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.repeatOnLifecycle
import androidx.navigation.fragment.navArgs
import dev.kamikaze.movike.R
import dev.kamikaze.movike.common.CollapsingToolbarFragment
import dev.kamikaze.movike.common.base.BaseUiState
import dev.kamikaze.movike.databinding.FragmentDetailMovieBinding
import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.presentation.customviews.WatchMovieBtn
import dev.kamikaze.movike.presentation.navigation.navigators.DetailsNavigator
import dev.kamikaze.movike.presentation.ui.viewmodel.DetailsMovieViewModel
import dev.kamikaze.shared_utils.extensions.setImg
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import javax.inject.Inject

class DetailsFragment : CollapsingToolbarFragment<DetailsNavigator>(), WatchMovieBtn.WatchCallback {
    
    private var _binding: FragmentDetailMovieBinding? = null
    private val binding get() = _binding!!
    
    @Inject
    lateinit var factory: ViewModelProvider.Factory
    private val viewModel: DetailsMovieViewModel by viewModels { factory }
    
    
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        _binding = FragmentDetailMovieBinding.inflate(inflater, container, false)
        return binding.root
    }
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                launch {
                    viewModel.uiState.collectLatest {
                        when (it) {
                            is BaseUiState.Success<*> -> onSuccessLoad(it.value as Movie)
                            is BaseUiState.Error -> showError(it.throwable)
                        }
                    }
                }
                launch {
                    viewModel.isWatchBtn.collectLatest { binding.watchMovie.renderSaveBtn(it) }
                }
            }
        }
    }
    
    private fun onSuccessLoad(movie: Movie) {
        onLoadFinish()
        renderUi(movie)
    }
    
    override fun onDestroyView() {
        super.onDestroyView()
        binding.watchMovie.callback = null
        _binding = null
    }
    
    override fun initView() {
        showProgress()
        val args: DetailsFragmentArgs by navArgs()
        viewModel.onLoadMovie(args.movieId)
    }
    
    override fun onWatchClicked() = viewModel.onSeeClick()
    
    override fun onRetryLoad() {
        initView()
    }
    
    private fun renderUi(movie: Movie) {
        val collapseImage = activity?.findViewById<ImageView>(R.id.toolbarIV)
        collapseImage?.setImg(movie.backdropPath)
        with(binding) {
            watchMovie.callback = this@DetailsFragment
            titleTV.text = movie.title
            ratingTV.apply {
                text = movie.ratingValue
                isVisible = movie.ratingValue != null
            }
            posterIV.setImg(movie.posterPath)
            overviewTV.text = movie.overview
        }
    }
    
}
