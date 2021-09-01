package dev.kamikaze.movike.presentation.ui.viewmodel

import androidx.lifecycle.MutableLiveData
import dev.kamikaze.movike.common.base.BaseViewModel
import dev.kamikaze.movike.repository.RepositoryImpl
import javax.inject.Inject

class ProfileViewModel
@Inject constructor(
    repository: RepositoryImpl
) : BaseViewModel() {

    val providerError = MutableLiveData(false)

    private val onErrorLoadPage: (Throwable) -> Unit
        get() = { providerError.postValue(true) }

}
