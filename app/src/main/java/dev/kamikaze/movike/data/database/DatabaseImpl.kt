package dev.kamikaze.movike.data.database

import dev.kamikaze.movike.R
import dev.kamikaze.movike.data.database.dao.CategoryFavoriteDao
import dev.kamikaze.movike.data.database.dao.CategoryMovieCrossRefDao
import dev.kamikaze.movike.data.database.dao.MovieDao
import dev.kamikaze.movike.models.room.entity.CategoryFavorite
import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.models.room.relate.CategoryWithMovies
import dev.kamikaze.movike.models.room.relate.MovieWithCategories
import dev.kamikaze.movike.utils.AppConstants
import dev.kamikaze.movike.utils.UIHelper
import javax.inject.Inject

class DatabaseImpl
@Inject constructor(
    private val movieTable: MovieDao,
    private val categoryTable: CategoryFavoriteDao,
    private val crossRefCategoryMovieTable: CategoryMovieCrossRefDao
) : DatabaseInterface {

    override val moviesWithCategory: List<MovieWithCategories>
        get() = movieTable.getList()

    override val categoriesFavorite: List<CategoryWithMovies>
        get() = categoryTable.getList()

    override fun saveMovieAsWatch(movie: Movie): Boolean {
        return saveFavoriteMovie(movie, AppConstants.DB_ID_CATEGORY_WATCH)
    }

    override fun initStartValue() {
        val categoryList = categoryTable.getList()
        if (categoryList.isEmpty()) {
            val categoryArray = UIHelper.getArray(R.array.categoryFavorite)
            val defaultCategoryList = categoryArray.flatMap {
                listOf(CategoryFavorite(categoryTitle = it))
            }
            categoryTable.insert(defaultCategoryList)
        }
    }

    override fun isWatchMovieCheck(movie: Movie): Boolean {
        return checkIsExistFavoriteMovie(movie, AppConstants.DB_ID_CATEGORY_WATCH)
    }

    private fun checkIsExistFavoriteMovie(viewedMovie: Movie, categoryId: Int): Boolean {
        val movieId = viewedMovie.id
        val movie = movieTable.getById(movieId)
        test()
        return if (movie == null) {
            false // return not exist if movie not found
        } else {  // if movie found
            val crossRefMovieCategory = crossRefCategoryMovieTable.getCrossRefMovieCategoryById(categoryId, movieId)
            crossRefMovieCategory != null // return true if found relate between movie and category
        }
    }

    private fun saveFavoriteMovie(viewedMovie: Movie, categoryId: Int): Boolean {
        val movieId = viewedMovie.id
        val movie = movieTable.getById(movieId)
        if (movie == null) { // if movie not found
            movieTable.insert(viewedMovie)
            crossRefCategoryMovieTable.insert(categoryId, movieId) // add relate movie with category
            test()
            return true
        } else {  // if movie found
            val crossRefMovieCategory = crossRefCategoryMovieTable.getCrossRefMovieCategoryById(categoryId, movieId)
            return if (crossRefMovieCategory == null) {  // if relation between the movie and category not found
                crossRefCategoryMovieTable.insert(categoryId, movieId)
                test()
                true
            } else { // if relation between the movie and category found
                crossRefCategoryMovieTable.delete(crossRefMovieCategory) // delete relation between tables
                val movieWithCategories = movieTable.getMovieWithCategoriesByMovieId(movieId)
                if (movieWithCategories.categoryList.isNullOrEmpty()) { // get categories of movie and check on empty
                    movieTable.delete(movie)
                } // if not empty, then not do anything, because there are other relate
                test()
                false
            }
        }
    }

    private fun test() {
        val test = movieTable.getList()
        val ar = crossRefCategoryMovieTable.getList()
        val arq = categoryTable.getList()
        arq
    }

}
