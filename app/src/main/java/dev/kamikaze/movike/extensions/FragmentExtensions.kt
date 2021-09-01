package dev.kamikaze.movike.extensions

import dev.kamikaze.movike.common.AutoDestroyValue
import dev.kamikaze.movike.common.base.BaseFragment
import dev.kamikaze.movike.common.base.BaseNavigator

fun <N : BaseNavigator, T> BaseFragment<N>.autoCleared() = AutoDestroyValue<N, T>(this)
