package dev.kamikaze.movike.models

import dev.kamikaze.movike.common.base.BaseEntityInterface
import kotlinx.serialization.Serializable

@Serializable
open class BaseEntity(

    override var id: Int = 0,
    override var name: String = ""

) : BaseEntityInterface
