package dev.kamikaze.movike.presentation.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.paging.PagingDataAdapter
import dev.kamikaze.movike.databinding.ListItemMovieBinding
import dev.kamikaze.movike.presentation.adapters.comparators.MovieAdapterComparator
import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.presentation.adapters.callbacks.MovieItemClickListener
import dev.kamikaze.movike.presentation.adapters.viewholders.MovieHolder
import javax.inject.Inject

class MovieAdapter
@Inject constructor() : PagingDataAdapter<Movie, MovieHolder>(MovieAdapterComparator()) {

    internal var callback: MovieItemClickListener? = null

    override fun onCreateViewHolder(parent: ViewGroup, codeViewType: Int) =
        MovieHolder(
            ListItemMovieBinding.inflate(
                LayoutInflater.from(parent.context), parent, false
            ), callback
        )

    override fun onBindViewHolder(holder: MovieHolder, pos: Int) {
        getItem(pos)?.let { holder.bind(it) }
    }

}
