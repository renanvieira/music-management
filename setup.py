from setuptools import setup

setup(
    name='music-collection',
    packages=['music_management'],
    include_package_data=True,
    install_requires=[
        'flask', 'sqlalchemy', 'alembic', 'requests'
    ],
)
