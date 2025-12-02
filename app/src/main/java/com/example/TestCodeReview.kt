package com.example

import android.content.Context
import androidx.lifecycle.ViewModel
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch

/**
 * Тестовый класс для демонстрации Code Review
 * Содержит различные проблемы для обнаружения
 */
class TestCodeReview : ViewModel() {

    // Проблема: Context в ViewModel
    private val context: Context? = null

    fun testFunction() {
        // Проблема: println в продакшн коде
        println("Debug message")

        // Проблема: Force unwrap
        val result = context!!.getString(android.R.string.ok)

        // TODO: Implement proper error handling
        try {
            someRiskyOperation()
        } catch (e: Exception) {
        }

        // Проблема: GlobalScope
        GlobalScope.launch {
            // Проблема: нет явного Dispatcher
            loadData()
        }

        // Можно улучшить: использовать let
        if (context != null) {
            context.getSystemService(Context.ACTIVITY_SERVICE)
        }
    }

    private fun someRiskyOperation() {
        // Simulated risky operation
    }

    private fun loadData() {
        // Simulated data loading
    }

    // FIXME: This needs refactoring
    fun anotherFunction() {
        val value1 = "test"
        val value2 = "test2"

        if (value1 == "test") {
            println("case 1")
        } else if (value1 == "test2") {
            println("case 2")
        } else if (value1 == "test3") {
            println("case 3")
        }
    }
}
