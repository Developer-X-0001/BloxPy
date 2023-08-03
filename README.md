# BloxPy: Your All-in-One Python API Wrapper for Roblox Development

BloxPy is the ultimate Python API wrapper for Roblox developers, offering an all-in-one solution to interact with Roblox Public APIs effortlessly. Whether you want to retrieve player data, manage groups, or create dynamic game interactions, BloxPy empowers you to build amazing Roblox experiences with ease.

[![PyPI Version](https://img.shields.io/pypi/v/BloxPy)](https://pypi.org/project/BloxPy/)
[![Python Version](https://img.shields.io/pypi/pyversions/BloxPy)](https://pypi.org/project/BloxPy/)

## Features

- Effortlessly interact with Roblox Public APIs.
- Retrieve player data, game information, and group details.
- Simplify group management tasks, such as handling members and roles.
- Create dynamic game interactions and enhance in-game experiences.

## Installation

You can install BloxPy using pip:

```bash
pip install -U BloxPy
```

## Usage

- ### Users
```py
from BloxPy import Users

# Fetch player data
player_id = 1234567890
player_data = Users.get_user(player_id)
print(player_data.name) # Username
print(player_data.displayName) # Display Name
```

- ### Groups
```py
from BloxPy import Groups

# Fetch group data
group_id = 1234567890
group_data = Groups.get_group(group_id)
print(group_data.name) # Group Name
print(group_data.memberCount) # Group Member Count
```

- ### Search
```py
from BloxPy import Search

# Fetch users by keyword
user_keyword = 'Henry'
user_search_results = Search.search_users(keyword)
print(user_search_results.data) # List containing data

for user in user_search_results.data:
    print(user.name) # Username
    print(user.id) # User ID

# Fetch groups by keyword
group_keyword = 'Roblox'
group_search_results = Search.search_groups(keyword)
print(group_search_results.data) # List containing data

for group in group_search_results.data:
    print(group.name) # Name
    print(group.description) # Description
    print(group.memberCount) # Member Count
```

## Documentation

For detailed documentation and usage examples, check out the [BloxPy Documentation](https://Developer-X-0001.github.io/BloxPy-docs).

## Contributing

We welcome contributions from the community! If you find a bug or have an enhancement in mind, please open an issue or submit a pull request.

## License

BloxPy is licensed under the MIT License. See the [LICENSE](https://github.com/Developer-X-0001/BloxPy/blob/main/LICENSE) file for details.

## Contact

For questions or support, you can reach out to us at [developer.x.business@gmail.com](mailto:developer.x.business@gmail.com) or join our [Official Discord server](https://discord.gg/EHEBFwe3fx).
