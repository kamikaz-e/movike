package dev.kamikaze.movike.common

import androidx.lifecycle.DefaultLifecycleObserver
import androidx.lifecycle.LifecycleOwner
import dev.kamikaze.movike.common.base.BaseFragment
import dev.kamikaze.movike.common.base.BaseNavigator
import kotlin.properties.ReadWriteProperty
import kotlin.reflect.KProperty

class AutoDestroyValue<N : BaseNavigator, T>(val fragment: BaseFragment<N>) : ReadWriteProperty<BaseFragment<N>, T> {

    private var _value: T? = null

    init {
        fragment.lifecycle.addObserver(object : DefaultLifecycleObserver {
            override fun onCreate(owner: LifecycleOwner) {
                fragment.viewLifecycleOwnerLiveData.observe(fragment) { viewLifecycleOwner ->
                    viewLifecycleOwner?.lifecycle?.addObserver(object : DefaultLifecycleObserver {
                        override fun onDestroy(owner: LifecycleOwner) {
                            _value = null
                        }
                    })
                }
            }
        })
    }

    override fun setValue(thisRef: BaseFragment<N>, property: KProperty<*>, value: T) {
        _value = value
    }

    override fun getValue(thisRef: BaseFragment<N>, property: KProperty<*>): T {
        return _value ?: throw IllegalStateException(
            "auto-cleared-value not be available"
        )
    }

}
