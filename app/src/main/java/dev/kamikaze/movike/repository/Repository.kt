package dev.kamikaze.movike.repository

import dev.kamikaze.movike.api.ApiService
import dev.kamikaze.movike.data.database.DatabaseInterface
import dev.kamikaze.movike.data.datasource.DataSourceInterface

interface Repository : DatabaseInterface, DataSourceInterface, ApiService