"""Setup file"""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="handelsraad_bot",
    version="0.0.1",
    author="Joost Sijm",
    author_email="joostsijm@gmail.com",
    description="Handelsraad bot",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/joostsijm/handelsraad_bot",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        "appdirs",
        "APScheduler",
        "pathlib2",
        "python-telegram-bot",
        "python-dotenv",
        "psycopg2-binary",
        "SQLAlchemy",
        "sqlalchemy-migrate",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
