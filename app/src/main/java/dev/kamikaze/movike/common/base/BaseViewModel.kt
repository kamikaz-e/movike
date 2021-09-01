package dev.kamikaze.movike.common.base

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import retrofit2.HttpException
import retrofit2.Response
import kotlin.coroutines.CoroutineContext

abstract class BaseViewModel : ViewModel() {

    fun <T : Any> safeApiCall(
        call: suspend () -> Response<T>,
        onSuccess: (T) -> Unit,
        onError: (Throwable) -> Unit
    ) {
        doCoroutineWork { request(call, onSuccess, onError) }
    }

    fun <P> doWork(doOnAsyncBlock: suspend CoroutineScope.() -> P) {
        doCoroutineWork(doOnAsyncBlock, viewModelScope, Dispatchers.IO)
    }

    fun <P> doWorkInMainThread(doOnAsyncBlock: suspend CoroutineScope.() -> P) {
        doCoroutineWork(doOnAsyncBlock, viewModelScope, Dispatchers.Main)
    }

    private inline fun <P> doCoroutineWork(crossinline doOnAsyncBlock: suspend CoroutineScope.() -> P) {
        viewModelScope.launch {
            withContext(coroutineContext) { doOnAsyncBlock.invoke(this) }
        }
    }

    private suspend fun <T : Any> request(
        call: suspend () -> Response<T>,
        onSuccess: (T) -> Unit,
        onError: ((Throwable) -> Unit)?
    ) {
        val response = call.invoke()
        if (response.isSuccessful) {
            response.body()?.let { onSuccess.invoke(it) }
        } else {
            onError?.invoke(HttpException(response))
        }
    }

    private inline fun <P> doCoroutineWork(
        crossinline doOnAsyncBlock: suspend CoroutineScope.() -> P,
        coroutineScope: CoroutineScope,
        context: CoroutineContext
    ) {
        coroutineScope.launch {
            withContext(context) {
                doOnAsyncBlock.invoke(this)
            }
        }
    }

    /*  fun <P> doRepeatWork(delayMs: Long, doOnAsyncBlock: suspend CoroutineScope.() -> P) {
      isActive = true
      viewModelScope.launch {
          while (this@BaseViewModel.isActive) {
              withContext(Dispatchers.IO) {
                  doOnAsyncBlock.invoke(this)
              }
              if (this@BaseViewModel.isActive) {
                  delay(delayMs)
              }
          }
      }
  }*/

}
