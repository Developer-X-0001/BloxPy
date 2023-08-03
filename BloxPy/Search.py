import requests
from dataclasses import dataclass
from typing import List, Optional
from _exceptions import (
    RobloxBadRequestError,
    RobloxRateLimitError,
    RobloxUnexpectedError,
    RobloxSearchTermLengthError,
    RobloxSearchTermEmptyError,
    RobloxSearchTermInappropriateError,
    RobloxSearchTermTooShort,
    RobloxSearchTermFilteredError
)

@dataclass
class UserSearchResult:
    previousUsernames: List[str]
    hasVerifiedBadge: bool
    id: int
    name: str
    displayName: str

@dataclass
class UserSearchResults:
    previousPageCursor: str
    nextPageCursor: str
    data: List[UserSearchResult]

def search_users(keyword: str, limit: Optional[int] = None, cursor: Optional[str] = None) -> UserSearchResults:
    """
    Searches for users by keyword.

    ## Args:
        keyword (str): The search keyword.
        limit (int): The number of results per request. (10, 25, 50, 100)
        cursor (str): The paging cursor for the previous or next page.

    ## Returns:
        List[SearchResult]: A list of SearchResult objects, each containing the search result properties.
    
    ### Raises:
        RobloxBadRequestError: If the request is invalid or malformed (HTTP status code 400).
        RobloxRateLimitError: If the API rate limit has been exceeded (HTTP status code 429).

    ### Example:
        >>> search('Henry', 10)
        [
            SearchResult(previousUsernames=[], hasVerifiedBadge=False, id=12345, name='Henry12', displayName='Henry The Tester'),
            SearchResult(previousUsernames=[], hasVerifiedBadge=True, id=67890, name='HenryTester', displayName='Henry Jr'),
            ...
        ]
    """
    base_url = f'https://users.roblox.com/v1/users/search?keyword={keyword}'

    if limit:
        limits = [10, 25, 50, 100]
        if limit not in limits:
            raise RobloxBadRequestError('Limit can only be 10, 25, 50, or 100')
        
        else:
            base_url += f"&limit={limit}"
    
    if cursor:
        base_url += f"&cursor={cursor}"
    
    response = requests.get(base_url, headers={'accept': 'application/json'})

    if response.status_code == 400:
        error_code = int(response.json()['errors'][0]['code'])
        error_message = (response.json()['errors'][0]['message'])
        if error_code == 5:
            raise RobloxSearchTermFilteredError(error_message)
        elif error_code == 6:
            raise RobloxSearchTermTooShort(error_message)
        else:
            raise RobloxBadRequestError(error_message)
    
    if response.status_code == 429:
        raise RobloxRateLimitError('Too many requests.')

    if response.status_code == 200:
        search_data = response.json()
        user_search_results = UserSearchResults(
            previousPageCursor=search_data.get('previousPageCursor', None),
            nextPageCursor=search_data.get('nextPageCursor', None),
            data=[
                UserSearchResult(
                    previousUsernames=item.get('previousUsernames', None),
                    hasVerifiedBadge=item.get('hasVerifiedBadge', None),
                    id=item.get('id', None),
                    name=item.get('name', None),
                    displayName=item.get('displayName', None)
                )
                for item in search_data['data']
            ]
        )
        return user_search_results

@dataclass
class GroupSearchResult:
    id: int
    name: str
    description: str
    memberCount: int
    previousName: str
    publicEntryAllowed: bool
    created: str
    updated: str
    hasVerifiedBadge: bool

@dataclass
class GroupSearchResults:
    previousPageCursor: str
    nextPageCursor: str
    data: List[GroupSearchResult]

def search_groups(keyword: str, limit: Optional[int] = None, cursor: Optional[str] = None, prioritizeExactMatch: Optional[bool] = False) -> GroupSearchResults:
    """
    Searches for groups by keyword.

    ## Args:
        keyword (str): The search keyword.
        limit (int): The number of results per request. (10, 25, 50, 100)
        cursor (str): The paging cursor for the previous or next page.
        prioritizeExactMatch (bool): Whether or not to prioritize the exact match for the keyword. (optional, defaults to False)

    ## Returns:
        GroupSearchResults: A GroupSearchResults object containing the search results and cursors.
    
    ### Raises:
        RobloxSearchTermError: Base exception class for search term errors.
        RobloxSearchTermInappropriateError: If the search term is not appropriate for Roblox (HTTP status code 2).
        RobloxSearchTermEmptyError: If the search term is left empty (HTTP status code 3).
        RobloxSearchTermLengthError: If the search term length is not within the required range (HTTP status code 4).
        RobloxBadRequestError: If the request is invalid or malformed (HTTP status code 400).
        RobloxRateLimitError: If the API rate limit has been exceeded (HTTP status code 429).

    ### Example:
        >>> search_groups('Roblox', limit=10)
        GroupSearchResults(previousPageCursor=None, nextPageCursor='some_cursor_value', data=[
            GroupSearchResult(id=123, name='Roblox Group 1', description='This is a group related to Roblox.', memberCount=100, previousName='PreviousName1', publicEntryAllowed=True, created='2023-07-30T21:12:47.212Z', updated='2023-07-30T21:12:47.212Z', hasVerifiedBadge=True),
            GroupSearchResult(id=456, name='Roblox Group 2', description='This is another group related to Roblox.', memberCount=200, previousName='PreviousName2', publicEntryAllowed=False, created='2023-07-30T21:12:47.212Z', updated='2023-07-30T21:12:47.212Z', hasVerifiedBadge=False),
            ...
        ])
    """
    base_url = f'https://groups.roblox.com/v1/groups/search?keyword={keyword}'

    if prioritizeExactMatch:
        base_url += "&prioritizeExactMatch=true"

    if limit:
        limits = [10, 25, 50, 100]
        if limit not in limits:
            raise RobloxBadRequestError('Limit can only be 10, 25, 50, or 100')
        else:
            base_url += f"&limit={limit}"

    if cursor:
        base_url += f"&cursor={cursor}"

    response = requests.get(base_url, headers={'accept': 'application/json'})

    if response.status_code == 400:
        error_code = int(response.json()['errors'][0]['code'])
        error_message = (response.json()['errors'][0]['message'])
        if error_code == 2:
            raise RobloxSearchTermInappropriateError(error_message)
        elif error_code == 3:
            raise RobloxSearchTermEmptyError(error_message)
        elif error_code == 4:
            raise RobloxSearchTermLengthError(error_message)
        else:
            raise RobloxBadRequestError(error_message)

    if response.status_code == 429:
        raise RobloxRateLimitError('Too many requests.')

    if response.status_code == 200:
        search_data = response.json()
        group_search_results = GroupSearchResults(
            previousPageCursor=search_data.get('previousPageCursor', None),
            nextPageCursor=search_data.get('nextPageCursor', None),
            data=[
                GroupSearchResult(
                    id=item.get('id', None),
                    name=item.get('name', None),
                    description=item.get('description', None),
                    memberCount=item.get('memberCount', None),
                    previousName=item.get('previousName', None),
                    publicEntryAllowed=item.get('publicEntryAllowed', None),
                    created=item.get('created', None),
                    updated=item.get('updated', None),
                    hasVerifiedBadge=item.get('hasVerifiedBadge', None)
                )
                for item in search_data['data']
            ]
        )
        return group_search_results
    else:
        raise RobloxUnexpectedError(f"Unexpected HTTP status code: {response.status_code}")