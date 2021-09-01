package dev.kamikaze.movike.presentation.adapters.viewholders

import androidx.core.view.isVisible
import androidx.paging.LoadState
import androidx.recyclerview.widget.RecyclerView
import dev.kamikaze.movike.presentation.customviews.error.ErrorCallback
import dev.kamikaze.movike.databinding.ListItemLoadingStateBinding
import dev.kamikaze.shared_error.ApiErrorFactory

class LoadStateViewHolder(
    private val binding: ListItemLoadingStateBinding,
    private val callback: ErrorCallback?
) : RecyclerView.ViewHolder(binding.root) {

    init {
        binding.retryTV.setOnClickListener { callback?.onRetryLoad() }
    }

    internal fun bind(loadState: LoadState) {
        with(binding) {
            progressBar.isVisible = loadState is LoadState.Loading
            retryTV.isVisible = loadState is LoadState.Error
            when (loadState) {
                is LoadState.Loading -> {
                    showTitles(false)
                }
                is LoadState.Error -> {
                    val error = ApiErrorFactory(itemView.context).handleError(loadState.error)
                    titleTV.text = error.titleText
                    subtitleTV.text = error.subtitleText
                    showTitles(true)
                }
                is LoadState.NotLoading -> {
                    // reached final page
                }
            }
        }
    }

    private fun showTitles(isVisible: Boolean) {
        binding.apply {
            titleTV.isVisible = isVisible
            subtitleTV.isVisible = isVisible
        }
    }

}