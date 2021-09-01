package dev.kamikaze.movike.utils

import androidx.paging.PagingConfig
import dev.kamikaze.movike.utils.AppConstants

object PagingConfigs {

    val defaultPagingConfig = PagingConfig(
        pageSize = AppConstants.PAGING_PAGE_SIZE,
        enablePlaceholders = false
    )
}