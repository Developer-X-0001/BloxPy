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
class OwnerData:
    buildersClubMembershipType: int
    hasVerifiedBadge: bool
    userId: int
    username: str
    displayName: str

@dataclass
class PosterData:
    buildersClubMembershipType: int
    hasVerifiedBadge: bool
    userId: int
    username: str
    displayName: str

@dataclass
class ShoutData:
    body: str
    poster: PosterData
    created: str
    updated: str

@dataclass
class RoleData:
    id: int
    name: str
    description: str
    rank: int
    memberCount: int

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
class GroupData:
    id: int
    name: str
    description: str
    owner: OwnerData
    shout: ShoutData
    memberCount: int
    isBuildersClubOnly: bool
    publicEntryAllowed: bool
    isLocked: bool
    hasVerifiedBadge: bool

    def roles(self) -> List[RoleData]:
        """
        Fetches a list of roles within the group represented by the current instance.

        ## Returns:
            List[RoleData]: A list of RoleData objects, each containing information about a role in the group, including its ID,
                            name, description, rank, and member count.
        
        ## Raises:
            RobloxNotFoundError: If the group is not found (HTTP status code 404).
            RobloxBadRequestError: If the request is invalid or malformed (HTTP status code 400).
            RobloxUnauthorizedError: If authentication is required and has failed or has not been provided (HTTP status code 401).
            RobloxRateLimitError: If the API rate limit has been exceeded (HTTP status code 429).
            RobloxInternalServerError: If the Roblox API encounters an internal server error (HTTP status code 500).
            RobloxUnexpectedError: If an unexpected HTTP status code is returned from the Roblox API.
            ValueError: If the JSON response is missing required properties or has unexpected values.
        
        ## Note:
            - The current instance must represent a valid group on Roblox for this function to work correctly.
            - The function returns a list of RoleData objects, each representing a role within the group.
            - Roles are hierarchical in a group, with the role having the lowest rank considered as the highest-ranking role
            (e.g., "Owners" usually have the lowest rank, while "Members" have higher ranks).
            - The returned RoleData objects provide information about each role, such as its name, description, rank, and the number
            of members holding that role.
        """
        base_url = f'https://groups.roblox.com/v1/groups/{self.id}/roles'
        
        response = requests.get(base_url)
        if response.status_code == 404:
            raise RobloxNotFoundError("Group not found.")
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
            roles_data = response.json()
            roles_list = [
                RoleData(
                    id=role.get('id', None),
                    name=role.get('name', None),
                    description=role.get('description', None),
                    rank=role.get('rank', None),
                    memberCount=role.get('memberCount', None)
                )
                for role in roles_data.get('roles', [])
            ]
            return roles_list
    
    def games(self, limit: Optional[int] = None, cursor: Optional[str] = None, sortOrder: Optional[str] = None) -> GamesResultData:
        """
        Fetches a list of games created by the group represented by the current instance.

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
            - The current instance must represent a valid group on Roblox for this function to work correctly.
            - If the 'limit' parameter is not provided, all games created by the group will be retrieved, which might take longer
            for groups with a large number of games.
            - The returned GamesResultData object provides pagination cursors, which can be used for subsequent requests
            to retrieve more games.
        """
        base_url = f'https://games.roblox.com/v2/groups/{self.id}/games?accessFilter=2'

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

def get_group(group_id: int) -> GroupData:
    """
    Returns detailed group information by ID.

    ## Args:
        group_id (int): ID of the Roblox Group

    ## Returns:
        GroupData: A GroupData object containing the group information
    
    ### Raises:
        RobloxNotFoundError: If the group is not found (HTTP status code 404).
        RobloxBadRequestError: If the request is invalid or malformed (HTTP status code 400).
        RobloxUnauthorizedError: If authentication is required and has failed or has not been provided (HTTP status code 401).
        RobloxRateLimitError: If the API rate limit has been exceeded (HTTP status code 429).
        RobloxInternalServerError: If the Roblox API encounters an internal server error (HTTP status code 500).
        RobloxUnexpectedError: If an unexpected HTTP status code is returned from the Roblox API.
        ValueError: If the JSON response is missing required properties or has unexpected values.

    ### Example:
        >>> get_group_data(1234567890)
        GroupData(id=1234567890, name='Example Group', description='This is an example group.', owner=OwnerData(...), shout=ShoutData(...), memberCount=100, isBuildersClubOnly=False, publicEntryAllowed=True, isLocked=False, hasVerifiedBadge=True)
    """
    response = requests.get(f'https://groups.roblox.com/v1/groups/{group_id}')

    if response.status_code == 404:
        raise RobloxNotFoundError("Group not found.")
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
        group_data = response.json()

        owner_data = group_data.get('owner')
        owner = None
        if owner_data:
            owner = OwnerData(
                buildersClubMembershipType=owner_data.get('buildersClubMembershipType', None),
                hasVerifiedBadge=owner_data.get('hasVerifiedBadge', None),
                userId=owner_data.get('userId', None),
                username=owner_data.get('username', None),
                displayName=owner_data.get('displayName', None)
            )

        shout_data = group_data.get('shout')
        shout = None
        if shout_data:
            poster_data = shout_data.get('poster')
            poster = None
            if poster_data:
                poster = PosterData(
                    buildersClubMembershipType=poster_data.get('buildersClubMembershipType', None),
                    hasVerifiedBadge=poster_data.get('hasVerifiedBadge', None),
                    userId=poster_data.get('userId', None),
                    username=poster_data.get('username', None),
                    displayName=poster_data.get('displayName', None)
                )

            shout = ShoutData(
                body=shout_data.get('body', None),
                poster=poster,
                created=shout_data.get('created', None),
                updated=shout_data.get('updated', None)
            )

        return GroupData(
            id=group_data.get('id', None),
            name=group_data.get('name', None),
            description=group_data.get('description', None),
            owner=owner,
            shout=shout,
            memberCount=group_data.get('memberCount', None),
            isBuildersClubOnly=group_data.get('isBuildersClubOnly', None),
            publicEntryAllowed=group_data.get('publicEntryAllowed', None),
            isLocked=group_data.get('isLocked', None),
            hasVerifiedBadge=group_data.get('hasVerifiedBadge', None)
        )