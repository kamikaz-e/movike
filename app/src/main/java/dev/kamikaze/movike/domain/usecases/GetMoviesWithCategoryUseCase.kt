package dev.kamikaze.movike.domain.usecases

import dev.kamikaze.movike.models.room.relate.MovieWithCategories
import dev.kamikaze.movike.repository.Repository
import javax.inject.Inject

class GetMoviesWithCategoryUseCase
@Inject constructor(private val repository: Repository) {

    operator fun invoke(): List<MovieWithCategories> = repository.moviesWithCategory
}