package dev.kamikaze.shared_error

interface ApiError {

    var titleText: String?

    var subtitleText: String?

    var httpCode: Int?

    var code: Int?

    var btnName: String?

}