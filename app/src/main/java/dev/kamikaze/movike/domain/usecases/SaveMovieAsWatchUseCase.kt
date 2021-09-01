package dev.kamikaze.movike.domain.usecases

import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.repository.Repository
import javax.inject.Inject

class SaveMovieAsWatchUseCase
@Inject constructor(private val repository: Repository) {

    operator fun invoke(movie: Movie): Boolean = repository.saveMovieAsWatch(movie)

}