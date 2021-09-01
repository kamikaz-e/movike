package dev.kamikaze.movike.data.preferences

object AppPreferences : PreferencesInterface {

    private const val PREF_API_KEY = "PREF_API_KEY"

    /*override var apiKey: String
        get() = pref.getString(PREF_API_KEY, "bfdc275b8577a736e7cd02b7ea45e335").toString()
        set(value) {
            pref.edit().putString(PREF_API_KEY, value).apply()
        }
*/
}
