from setuptools import setup, find_packages

setup(
    name='rss-feed-parser',
    version='0.1.0',
    description='An RSS feed parser with Auth0-secured FastAPI',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'psycopg2-binary',
        'python-jose[cryptography]',
        'python-multipart',
        'passlib[bcrypt]',
        'feedparser',
        'httpx',
    ],
    include_package_data=True,
    zip_safe=False,
)
