import requests
from dataclasses import dataclass
from _exceptions import (
    RobloxNotFoundError,
    RobloxBadRequestError,
    RobloxUnauthorizedError,
    RobloxRateLimitError,
    RobloxInternalServerError,
    RobloxUnexpectedError
)

@dataclass
class UserData:
    description: str
    created: str
    isBanned: bool
    externalAppDisplayName: str
    hasVerifiedBadge: bool
    id: int
    name: str
    displayName: str

def get_user(user_id: int) -> UserData:
    """
    Returns detailed user information by ID.

    ## Args:
        user_id (int): ID of the Roblox User
    
    ## Returns:
        UserData: A UserData object containing the user information
    
    ### Raises:
        RobloxNotFoundError: If the user is not found (HTTP status code 404).
        RobloxBadRequestError: If the request is invalid or malformed (HTTP status code 400).
        RobloxUnauthorizedError: If authentication is required and has failed or has not been provided (HTTP status code 401).
        RobloxRateLimitError: If the API rate limit has been exceeded (HTTP status code 429).
        RobloxInternalServerError: If the Roblox API encounters an internal server error (HTTP status code 500).
        RobloxUnexpectedError: If an unexpected HTTP status code is returned from the Roblox API.
        ValueError: If the JSON response is missing required properties or has unexpected values.

    ### Example:
        >>> get_user(900673686)
        UserData(description='OMG is this u??? https://www.roblox.com/User.aspx?lD=', created='2018-12-22T06:14:46.327Z', isBanned=False, externalAppDisplayName=None, hasVerifiedBadge=False, id=900673686, name='TomClancy247', displayName='Steve')
    """
    response = requests.get(f'https://users.roblox.com/v1/users/{user_id}', headers={'accept': 'application/json'})

    if response.status_code == 404:
        raise RobloxNotFoundError("User not found.")
    elif response.status_code == 400:
        raise RobloxBadRequestError("Bad request.")
    elif response.status_code == 401:
        raise RobloxUnauthorizedError("Unauthorized. Authentication required.")
    elif response.status_code == 429:
        raise RobloxRateLimitError("Rate limit exceeded. Please try again later.")
    elif response.status_code == 500:
        raise RobloxInternalServerError("Internal server error.")
    elif response.status_code != 200:
        raise RobloxUnexpectedError(f"Unexpected HTTP status code: {response.status_code}")
    else:
        user_data = response.json()
        return UserData(
            description=user_data.get('description', None),
            created=user_data.get('created', None),
            isBanned=user_data.get('isBanned', None),
            externalAppDisplayName=user_data.get('externalAppDisplayName', None),
            hasVerifiedBadge=user_data.get('hasVerifiedBadge', None),
            id=user_data.get('id', None),
            name=user_data.get('name', None),
            displayName=user_data.get('displayName', None)
        )
    