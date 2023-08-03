import requests
from dataclasses import dataclass
from typing import List, Optional
from _exceptions import (
    RobloxNotFoundError,
    RobloxBadRequestError,
    RobloxUnauthorizedError,
    RobloxRateLimitError,
    RobloxInternalServerError,
    RobloxUnexpectedError
)

@dataclass
class FollowerData:
    isOnline: bool
    presenceType: int
    isDeleted: bool
    friendFrequentScore: int
    friendFrequentRank: int
    hasVerifiedBadge: bool
    description: str
    created: str
    isBanned: bool
    externalAppDisplayName: str
    id: int
    name: str
    displayName: str

@dataclass
class FollowersResultData:
    previousPageCursor: str
    nextPageCursor: str
    data: List[FollowerData]

@dataclass
class FollowingData:
    isOnline: bool
    presenceType: int
    isDeleted: bool
    friendFrequentScore: int
    friendFrequentRank: int
    hasVerifiedBadge: bool
    description: str
    created: str
    isBanned: bool
    externalAppDisplayName: str
    id: int
    name: str
    displayName: str

@dataclass
class FollowingsResultData:
    previousPageCursor: str
    nextPageCursor: str
    data: List[FollowingData]

@dataclass
class FriendData:
    isOnline: bool
    presenceType: int
    isDeleted: bool
    friendFrequentScore: int
    friendFrequentRank: int
    hasVerifiedBadge: bool
    description: str
    created: str
    isBanned: bool
    externalAppDisplayName: str
    id: int
    name: str
    displayName: str

@dataclass
class GameCreatorData:
    id: int
    type: int
    name: str

@dataclass
class GameRootPlaceData:
    id: int
    type: int
    name: str

@dataclass
class GameData:
    id: int
    name: str
    description: str
    creator: GameCreatorData
    rootPlace: GameRootPlaceData
    created: str
    updated: str
    placeVisits: int

@dataclass
class GamesResultData:
    previousPageCursor: str
    nextPageCursor: str
    data: List[GameData]

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

    def followers(self, limit: Optional[int] = None, cursor: Optional[str] = None, sortOrder: Optional[str] = None) -> FollowersResultData:
        """
        Fetches a list of followers for the user represented by the current instance.

        ## Args:
            limit (Optional[int]): The maximum number of followers to retrieve. Valid values are 10, 25, 50, or 100.\
                                If not provided, all followers will be retrieved.
            cursor (Optional[str]): A cursor to paginate through the list of followers. If provided, the API will return\
                                followers starting from the position after this cursor.
            sortOrder (Optional[str]): The order in which the followers should be sorted. Valid values are 'Asc' or 'Desc'.\
                                If 'Asc' is specified, followers will be returned in ascending order of creation time.\
                                If 'Desc' is specified, followers will be returned in descending order of creation time.

        ## Returns:
            FollowersResultData: An object containing the search results, including the list of followers, their online status,\
                                presence type, creation time, and more.
        
        ## Raises:
            RobloxBadRequestError: If the provided limit or sortOrder values are invalid.
            RobloxRateLimitError: If too many requests are made in a short period of time.
        
        ## Note:
            - The current instance must represent a valid user on Roblox for this function to work correctly.
            - If the 'limit' parameter is not provided, all followers of the user will be retrieved, which might take longer
            for users with a large number of followers.
            - The returned FollowersResultData object provides pagination cursors, which can be used for subsequent requests
            to retrieve more followers.
        """
        base_url = f'https://friends.roblox.com/v1/users/{self.id}/followers'

        if limit:
            limits = [10, 25, 50, 100]
            if limit not in limits:
                raise RobloxBadRequestError('Limit can only be 10, 25, 50 or 100')
            
            else:
                base_url += f"&limit={limit}"
        
        if sortOrder:
            Orders = ['Asc', 'Desc']
            if sortOrder not in Orders:
                raise RobloxBadRequestError('Sort order can only be either \'Asc\' or \'Desc\'')
            
            else:
                base_url += f"&sortOrder={sortOrder}"

        if cursor:
            base_url += f"&cursor={cursor}"
        
        response = requests.get(base_url, headers={'accept': 'application/json'})
    
        if response.status_code == 400:
            error_message = (response.json()['errors'][0]['message'])
            raise RobloxBadRequestError(error_message)
        
        if response.status_code == 429:
            raise RobloxRateLimitError('Too many requests.')

        if response.status_code == 200:
            search_data = response.json()
            followers_search_results = FollowersResultData(
                previousPageCursor=search_data.get('previousPageCursor', None),
                nextPageCursor=search_data.get('nextPageCursor', None),
                data=[
                    FollowerData(
                        isOnline=item.get('isOnline', None),
                        presenceType=item.get('presenceType', None),
                        isDeleted=item.get('isDeleted', None),
                        friendFrequentScore=item.get('friendFrequentScore', None),
                        friendFrequentRank=item.get('friendFrequentRank', None),
                        hasVerifiedBadge=item.get('hasVerifiedBadge', None),
                        description=item.get('description', None),
                        created=item.get('created', None),
                        isBanned=item.get('isBanned', None),
                        externalAppDisplayName=item.get('externalAppDisplayName', None),
                        id=item.get('id', None),
                        name=item.get('name', None),
                        displayName=item.get('displayName', None)
                    )
                    for item in search_data['data']
                ]
            )
            return followers_search_results
    
    def followings(self, limit: Optional[int] = None, cursor: Optional[str] = None, sortOrder: Optional[str] = None) -> FollowingsResultData:
        """
        Fetches a list of users followed by the user represented by the current instance.

        ## Args:
            limit (Optional[int]): The maximum number of followings to retrieve. Valid values are 10, 25, 50, or 100.\
                                If not provided, all followings will be retrieved.
            cursor (Optional[str]): A cursor to paginate through the list of followings. If provided, the API will return\
                                followings starting from the position after this cursor.
            sortOrder (Optional[str]): The order in which the followings should be sorted. Valid values are 'Asc' or 'Desc'.\
                                If 'Asc' is specified, followings will be returned in ascending order of creation time.\
                                If 'Desc' is specified, followings will be returned in descending order of creation time.

        ## Returns:
            FollowingsResultData: An object containing the search results, including the list of followings, their online status,\
                presence type, creation time, and more.
        
        ## Raises:
            RobloxBadRequestError: If the provided limit or sortOrder values are invalid.
            RobloxRateLimitError: If too many requests are made in a short period of time.
        
        ## Note:
            - The current instance must represent a valid user on Roblox for this function to work correctly.
            - If the 'limit' parameter is not provided, all followings of the user will be retrieved, which might take longer
            for users with a large number of followings.
            - The returned FollowingsResultData object provides pagination cursors, which can be used for subsequent requests
            to retrieve more followings.
        """
        base_url = f'https://friends.roblox.com/v1/users/{self.id}/followings'

        if limit:
            limits = [10, 25, 50, 100]
            if limit not in limits:
                raise RobloxBadRequestError('Limit can only be 10, 25, 50 or 100')
            
            else:
                base_url += f"&limit={limit}"
        
        if sortOrder:
            Orders = ['Asc', 'Desc']
            if sortOrder not in Orders:
                raise RobloxBadRequestError('Sort order can only be either \'Asc\' or \'Desc\'')
            
            else:
                base_url += f"&sortOrder={sortOrder}"

        if cursor:
            base_url += f"&cursor={cursor}"
        
        response = requests.get(base_url, headers={'accept': 'application/json'})
    
        if response.status_code == 400:
            error_message = (response.json()['errors'][0]['message'])
            raise RobloxBadRequestError(error_message)
        
        if response.status_code == 429:
            raise RobloxRateLimitError('Too many requests.')

        if response.status_code == 200:
            search_data = response.json()
            followings_search_results = FollowingsResultData(
                previousPageCursor=search_data.get('previousPageCursor', None),
                nextPageCursor=search_data.get('nextPageCursor', None),
                data=[
                    FollowingData(
                        isOnline=item.get('isOnline', None),
                        presenceType=item.get('presenceType', None),
                        isDeleted=item.get('isDeleted', None),
                        friendFrequentScore=item.get('friendFrequentScore', None),
                        friendFrequentRank=item.get('friendFrequentRank', None),
                        hasVerifiedBadge=item.get('hasVerifiedBadge', None),
                        description=item.get('description', None),
                        created=item.get('created', None),
                        isBanned=item.get('isBanned', None),
                        externalAppDisplayName=item.get('externalAppDisplayName', None),
                        id=item.get('id', None),
                        name=item.get('name', None),
                        displayName=item.get('displayName', None)
                    )
                    for item in search_data['data']
                ]
            )
            return followings_search_results
    
    def friends(self) -> List[FriendData]:
        """
        Fetches a list of friends for the user represented by the current instance.

        ## Returns:
            List[FriendData]: A list of FriendData objects, each containing information about a friend, such as their online status,\
                        presence type, creation time, and more.
        
        ## Raises:
            RobloxRateLimitError: If too many requests are made in a short period of time.
        
        ## Note:
            - The current instance must represent a valid user on Roblox for this function to work correctly.
            - The function returns all friends of the user without any pagination.
        """
        base_url = f'https://friends.roblox.com/v1/users/{self.id}/friends'
        
        response = requests.get(base_url, headers={'accept': 'application/json'})
    
        if response.status_code == 400:
            error_message = (response.json()['errors'][0]['message'])
            raise RobloxBadRequestError(error_message)
        
        if response.status_code == 429:
            raise RobloxRateLimitError('Too many requests.')

        if response.status_code == 200:
            search_data = response.json()
            friends_data = [
                    FriendData(
                        isOnline=item.get('isOnline', None),
                        presenceType=item.get('presenceType', None),
                        isDeleted=item.get('isDeleted', None),
                        friendFrequentScore=item.get('friendFrequentScore', None),
                        friendFrequentRank=item.get('friendFrequentRank', None),
                        hasVerifiedBadge=item.get('hasVerifiedBadge', None),
                        description=item.get('description', None),
                        created=item.get('created', None),
                        isBanned=item.get('isBanned', None),
                        externalAppDisplayName=item.get('externalAppDisplayName', None),
                        id=item.get('id', None),
                        name=item.get('name', None),
                        displayName=item.get('displayName', None)
                    )
                    for item in search_data['data']
                ]
            return friends_data
    
    def games(self, limit: Optional[int] = None, cursor: Optional[str] = None, sortOrder: Optional[str] = None) -> GamesResultData:
        """
        Fetches a list of games created by the user represented by the current instance.

        ## Args:
            limit (Optional[int]): The maximum number of games to retrieve. Valid values are 10, 25, 50, or 100.\
                                If not provided, all games will be retrieved.
            cursor (Optional[str]): A cursor to paginate through the list of games. If provided, the API will return\
                                games starting from the position after this cursor.
            sortOrder (Optional[str]): The order in which the games should be sorted. Valid values are 'Asc' or 'Desc'.\
                                If 'Asc' is specified, games will be returned in ascending order of creation time.\
                                If 'Desc' is specified, games will be returned in descending order of creation time.

        ## Returns:
            GamesResultData: An object containing the search results, including the list of games, their descriptions, creation time,\
                            and more.
        
        ## Raises:
            RobloxBadRequestError: If the provided limit or sortOrder values are invalid.
            RobloxRateLimitError: If too many requests are made in a short period of time.
        
        ## Note:
            - The current instance must represent a valid user on Roblox for this function to work correctly.
            - If the 'limit' parameter is not provided, all games created by the user will be retrieved, which might take longer
            for users with a large number of games.
            - The returned GamesResultData object provides pagination cursors, which can be used for subsequent requests
            to retrieve more games.
        """
        base_url = f'https://games.roblox.com/v2/users/{self.id}/games?accessFilter=2'

        if limit:
            limits = [10, 25, 50, 100]
            if limit not in limits:
                raise RobloxBadRequestError('Limit can only be 10, 25, 50 or 100')
            
            else:
                base_url += f"&limit={limit}"
        
        if sortOrder:
            Orders = ['Asc', 'Desc']
            if sortOrder not in Orders:
                raise RobloxBadRequestError('Sort order can only be either \'Asc\' or \'Desc\'')
            
            else:
                base_url += f"&sortOrder={sortOrder}"

        if cursor:
            base_url += f"&cursor={cursor}"
        
        response = requests.get(base_url, headers={'accept': 'application/json'})
    
        if response.status_code == 400:
            error_message = (response.json()['errors'][0]['message'])
            raise RobloxBadRequestError(error_message)
        
        if response.status_code == 429:
            raise RobloxRateLimitError('Too many requests.')

        if response.status_code == 200:
            search_data = response.json()

            creator_data = search_data['data'].get('creator')
            creator = None
            if creator_data:
                creator = GameCreatorData(
                    id=search_data['data'].get('id', None),
                    type=search_data['data'].get('type', None),
                    name=search_data['data'].get('name', None)
                )
            
            rootPlace_data = search_data['data'].get('rootPlace')
            rootPlace = None
            if rootPlace_data:
                rootPlace = GameRootPlaceData(
                    id=search_data['data'].get('id', None),
                    type=search_data['data'].get('type', None),
                    name=search_data['data'].get('name', None)
                )

            gamess_search_results = GamesResultData(
                previousPageCursor=search_data.get('previousPageCursor', None),
                nextPageCursor=search_data.get('nextPageCursor', None),
                data=[
                    GameData(
                        id=item.get('id', None),
                        name=item.get('name', None),
                        description=item.get('description', None),
                        creator=creator,
                        rootPlace=rootPlace,
                        created=item.get('created', None),
                        updated=item.get('updated', None),
                        placeVisits=item.get('placeVisits', None)
                    )
                    for item in search_data['data']
                ]
            )
            return gamess_search_results

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