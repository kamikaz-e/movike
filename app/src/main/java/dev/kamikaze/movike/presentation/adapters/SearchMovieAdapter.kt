package dev.kamikaze.movike.presentation.adapters

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.paging.PagingDataAdapter
import dev.kamikaze.movike.databinding.ListItemSearchMovieBinding
import dev.kamikaze.movike.presentation.adapters.comparators.MovieAdapterComparator
import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.presentation.adapters.viewholders.SearchMovieHolder
import dev.kamikaze.movike.presentation.adapters.callbacks.SearchMovieItemClickListener
import javax.inject.Inject

class SearchMovieAdapter
@Inject constructor() : PagingDataAdapter<Movie, SearchMovieHolder>(MovieAdapterComparator()) {

    internal var callback: SearchMovieItemClickListener? = null

    override fun onCreateViewHolder(parent: ViewGroup, codeViewType: Int) =
        SearchMovieHolder(
            ListItemSearchMovieBinding.inflate(
                LayoutInflater.from(parent.context), parent, false
            ), callback
        )

    override fun onBindViewHolder(holder: SearchMovieHolder, pos: Int) {
        getItem(pos)?.let { holder.bind(it) }
    }

}

