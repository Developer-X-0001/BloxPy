import requests
from dataclasses import dataclass
from typing import List
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