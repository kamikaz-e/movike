@file:Suppress("unused")

package dev.kamikaze.shared_utils.extensions

import android.widget.ImageView
import coil.load
import coil.transform.RoundedCornersTransformation

fun ImageView.setImg(image: String?) {
    load(image) {
        crossfade(true)
    }
}

fun ImageView.setImgWithRoundCorners(image: String?) {
    load(image) {
        crossfade(true)
        transformations(
            RoundedCornersTransformation(topLeft = 20f, topRight = 20f, bottomLeft = 20f, bottomRight = 20f)
        )
    }
}

/*
fun ImageView.initImage(image: String?) {
    Glide.with(this)
        .load(image)
        .error(R.drawable.ic_empty_image)
        .into(this)
}
*/

/*
fun ImageView.initImage(image: String?) {
    Picasso.get()
        .load(image)
        .error(R.drawable.ic_empty_image)
        .into(this)
}*/
