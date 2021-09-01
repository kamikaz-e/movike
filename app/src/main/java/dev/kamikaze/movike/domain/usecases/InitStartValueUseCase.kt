package dev.kamikaze.movike.domain.usecases

import dev.kamikaze.movike.repository.Repository
import javax.inject.Inject

class InitStartValueUseCase
@Inject constructor(private val repository: Repository) {

    operator fun invoke() = repository.initStartValue()

}