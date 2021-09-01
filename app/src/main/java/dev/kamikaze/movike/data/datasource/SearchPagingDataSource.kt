package dev.kamikaze.movike.data.datasource

import androidx.paging.PagingSource
import androidx.paging.PagingState
import dev.kamikaze.movike.api.ApiService
import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.utils.AppConstants
import java.io.IOException

class SearchPagingDataSource(
    private val apiService: ApiService,
    private  val searchString: String
) : PagingSource<Int, Movie>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Movie> {
        if (searchString.isEmpty()) return LoadResult.Page(
            data = emptyList(),
            prevKey = null,
            nextKey = null
        )
        var page = params.key ?: AppConstants.PAGING_DEFAULT_START_PAGE
        if (page == 0) {
            page = AppConstants.PAGING_DEFAULT_START_PAGE
        }
        return try {
            val data = apiService.apiSearchMovie(searchString, page)
            val prevKey = if (page == AppConstants.PAGING_DEFAULT_START_PAGE) null else page - 1
            val nextKey = if (page >= data.total_pages) null else page + 1
            LoadResult.Page(
                data = data.itemList,
                prevKey = prevKey,
                nextKey = nextKey
            )
        } catch (throwable: Throwable) {
            var exception = throwable
            if (throwable is IOException) {
                exception = IOException(throwable)
            }
            LoadResult.Error(exception)
        }
    }

    override fun getRefreshKey(state: PagingState<Int, Movie>) = state.anchorPosition

}