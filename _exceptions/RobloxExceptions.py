class RobloxApiError(Exception):
    """Base exception class for errors related to Roblox API."""

class RobloxNotFoundError(RobloxApiError):
    """Raised when the requested resource is not found (HTTP status code 404)."""

class RobloxBadRequestError(RobloxApiError):
    """Raised when the request is invalid or malformed (HTTP status code 400)."""

class RobloxUnauthorizedError(RobloxApiError):
    """Raised when authentication is required and has failed or has not been provided (HTTP status code 401)."""

class RobloxRateLimitError(RobloxApiError):
    """Raised when the API rate limit has been exceeded (HTTP status code 429)."""

class RobloxInternalServerError(RobloxApiError):
    """Raised when the Roblox API encounters an internal server error (HTTP status code 500)."""

class RobloxUnexpectedError(RobloxApiError):
    """Raised when an unexpected HTTP status code is returned from the Roblox API."""

class RobloxSearchTermError(RobloxApiError):
    """Base exception class for search term errors."""

class RobloxSearchTermInappropriateError(RobloxSearchTermError):
    """Raised when the search term is not appropriate for Roblox (HTTP status code 2)."""

class RobloxSearchTermEmptyError(RobloxSearchTermError):
    """Raised when the search term is left empty (HTTP status code 3)."""

class RobloxSearchTermLengthError(RobloxSearchTermError):
    """Raised when the search term length is not within the required range (HTTP status code 4)."""

class RobloxSearchTermFilteredError(RobloxSearchTermError):
    """Raised when the search term is filtered by Roblox (HTTP status code 5)"""

class RobloxSearchTermTooShort(RobloxSearchTermError):
    """Raised when the search term is too short (HTTP status code 6)"""