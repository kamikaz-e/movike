package dev.kamikaze.movike.common.base

import androidx.room.PrimaryKey
import kotlinx.serialization.Serializable

@Serializable
open class BaseEntity(
    @PrimaryKey(autoGenerate = true)
    override var id: Int = 0,
    override var name: String = ""
) : BaseEntityInterface
