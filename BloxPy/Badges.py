import requests
from dataclasses import dataclass
from _exceptions import (
    RobloxNotFoundError,
    RobloxUnexpectedError
)

@dataclass
class BadgeStatistics:
    pastDayAwardedCount: int
    awardedCount: int
    winRatePercentage: int

@dataclass
class BadgeAwardingUniverse:
    id: int
    name: str
    rootPlaceId: int

@dataclass
class BadgeData:
    id: int
    name: str
    description: str
    displayName: str
    displayDescription: str
    enabled: bool
    iconImageId: int
    displayIconImageId: int
    created: str
    updated: str
    statistics: BadgeStatistics
    awardingUniverse: BadgeAwardingUniverse

def get_badge(badge_id: int) -> BadgeData:
    """
    Fetches detailed information about a badge by its ID.

    ## Args:
        badge_id (int): The ID of the Roblox badge to retrieve.

    ## Returns:
        BadgeData: A BadgeData object containing information about the badge, including its ID, name, description, display name,\
                display description, whether it is enabled, icon image IDs, creation and update timestamps, statistics,\
                and the universe where the badge was awarded.

    ## Raises:
        RobloxNotFoundError: If the badge is invalid or does not exist (HTTP status code 404).
        RobloxUnexpectedError: If an unexpected HTTP status code is returned from the Roblox API.

    ## Note:
        - The function fetches the badge data from the Roblox API using the provided badge_id.
        - If the badge is found, it extracts the relevant information from the JSON response and creates a BadgeData object.
        - The returned BadgeData object contains detailed information about the badge, including its name, description,
          display name, and display description, along with other properties such as enabled status, icon image IDs, creation
          and update timestamps, badge statistics (including the number of awards in the past day, total awards, and win rate
          percentage), and the universe where the badge was awarded.
    """
    response = requests.get(f'https://badges.roblox.com/v1/badges/{badge_id}')

    if response.status_code == 404:
        raise RobloxNotFoundError('Badge is invalid or does not exist.')
    elif response.status_code != 200:
        raise RobloxUnexpectedError(f'Unexpected HTTP status code: {response.status_code}')
    else:
        badge_data = response.json()

        statistics_data = badge_data['statistics']
        statistics = None
        if statistics_data:
            statistics = BadgeStatistics(
                pastDayAwardedCount=badge_data['statistics']['pastDayAwardedCount'],
                awardedCount=badge_data['statistics']['awardedCount'],
                winRatePercentage=badge_data['statistics']['winRatePercentage']
            )
        
        awardingUniverse_data = badge_data['awardingUniverse']
        awardingUniverse = None
        if awardingUniverse_data:
            awardingUniverse = BadgeAwardingUniverse(
                id=badge_data['awardingUniverse']['id'],
                name=badge_data['awardingUniverse']['name'],
                rootPlaceId=badge_data['awardingUniverse']['rootPlaceId']
            )
        
        return BadgeData(
            id=badge_data.get('id', None),
            name=badge_data.get('name', None),
            description=badge_data.get('description', None),
            displayName=badge_data.get('displayName', None),
            displayDescription=badge_data.get('displayDescription', None),
            enabled=badge_data.get('enabled', None),
            iconImageId=badge_data.get('iconImageId', None),
            displayIconImageId=badge_data.get('displayIconImageId', None),
            created=badge_data.get('created', None),
            updated=badge_data.get('updated', None),
            statistics=statistics,
            awardingUniverse=awardingUniverse
        )