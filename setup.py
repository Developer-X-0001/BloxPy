from setuptools import setup, find_packages

NAME = 'BloxPy'
VERSION = '0.1.12'
DESCRIPTION = 'BloxPy: Your All-in-One Python API wrapper for Roblox Development'
LONG_DESCRIPTION = 'BloxPy is the ultimate Python API wrapper for Roblox developers, offering an all-in-one solution to interact with Roblox Public APIs effortlessly. Whether you want to retrieve player data, manage groups, or create dynamic game interactions, BloxPy empowers you to build amazing Roblox experiences with ease.'
AUTHOR = 'Developer X'
EMAIL = 'developer.x.business@gmail.com'
URL = 'https://github.com/Developer-X-0001/BloxPy'
LICENSE = 'MIT'
PYTHON_REQUIRES = '>=3.9'

with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

REQUIRES = [
    'requests', 
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=LICENSE,
    python_requires=PYTHON_REQUIRES,
    packages=find_packages(exclude=['tests']), 
    install_requires=REQUIRES,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
