@file:Suppress("unused")

package dev.kamikaze.shared_utils.extensions

import android.app.Activity
import android.content.Intent
import android.net.Uri
import androidx.core.app.ShareCompat

fun Activity.intentShareText(text: String) {
    val shareIntent = ShareCompat.IntentBuilder(this)
        .setText(text)
        .setType("text/plain")
        .createChooserIntent()
        .addFlags(Intent.FLAG_ACTIVITY_NEW_DOCUMENT or Intent.FLAG_ACTIVITY_MULTIPLE_TASK)
    startActivity(shareIntent)
}

fun Activity.intentOpenWebsite(url: String) {
    val openURL = Intent(Intent.ACTION_VIEW)
    openURL.data = Uri.parse(url)
    startActivity(openURL)
}
