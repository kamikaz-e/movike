package dev.kamikaze.movike.presentation.adapters.viewholders

import androidx.recyclerview.widget.RecyclerView
import dev.kamikaze.movike.databinding.ListItemSearchMovieBinding
import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.presentation.adapters.callbacks.SearchMovieItemClickListener
import dev.kamikaze.shared_utils.extensions.setImg

class SearchMovieHolder(
    private val binding: ListItemSearchMovieBinding,
    private val callback: SearchMovieItemClickListener?
) : RecyclerView.ViewHolder(binding.root) {

    internal fun bind(item: Movie) = with(binding) {
        initCallbacks(item)
        posterIV.setImg(item.posterPath)
        titleTV.text = item.title
        yearTv.text = item.yearValue
        ratingTV.text = item.ratingValue
        // ratingTV.isVisible = item.ratingValue != null
    }

    private fun ListItemSearchMovieBinding.initCallbacks(item: Movie) {
        //  optionsIV.setOnClickListener { callback.onOptionsClicked(item, layoutPosition) }
        itemView.setOnClickListener { callback?.onMovieClicked(item.id) }
        movieActionBtn.setOnClickListener { }
    }

}