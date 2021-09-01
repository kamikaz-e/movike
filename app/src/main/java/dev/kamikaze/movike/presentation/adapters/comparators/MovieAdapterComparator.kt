package dev.kamikaze.movike.presentation.adapters.comparators

import androidx.recyclerview.widget.DiffUtil
import dev.kamikaze.movike.models.room.entity.Movie

class MovieAdapterComparator : DiffUtil.ItemCallback<Movie>() {

    override fun areItemsTheSame(oldItem: Movie, newItem: Movie) = oldItem.id == newItem.id

    override fun areContentsTheSame(oldItem: Movie, newItem: Movie) = oldItem == newItem

}