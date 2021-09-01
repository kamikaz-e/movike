package dev.kamikaze.movike.presentation.adapters.viewholders

import androidx.recyclerview.widget.RecyclerView
import dev.kamikaze.movike.databinding.ListItemMovieBinding
import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.presentation.adapters.callbacks.MovieItemClickListener
import dev.kamikaze.shared_utils.extensions.setImgWithRoundCorners

class MovieHolder(
    private val binding: ListItemMovieBinding,
    private val callback: MovieItemClickListener?
) : RecyclerView.ViewHolder(binding.root) {

    internal fun bind(item: Movie) = with(binding) {
        initCallbacks(item)
        posterIV.apply {
            setImgWithRoundCorners(item.posterPath)
        }
        titleTV.text = item.title
        overviewTV.text = item.overview
    }

    private fun initCallbacks(item: Movie) {
        itemView.setOnClickListener { callback?.onMovieClicked(item.id) }
    }

}