package dev.kamikaze.movike.presentation.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.paging.LoadState
import androidx.paging.LoadStateAdapter
import dev.kamikaze.movike.presentation.customviews.error.ErrorCallback
import dev.kamikaze.movike.databinding.ListItemLoadingStateBinding
import dev.kamikaze.movike.presentation.adapters.viewholders.LoadStateViewHolder
import javax.inject.Inject

class LoadingStateAdapter @Inject constructor() :
    LoadStateAdapter<LoadStateViewHolder>() {

    var callback: ErrorCallback? = null

    override fun onCreateViewHolder(parent: ViewGroup, loadState: LoadState) =
        LoadStateViewHolder(
            ListItemLoadingStateBinding.inflate(
                LayoutInflater.from(parent.context), parent, false
            ), callback
        )

    override fun onBindViewHolder(holder: LoadStateViewHolder, loadState: LoadState) = holder.bind(loadState)

}