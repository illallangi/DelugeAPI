import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="illallangi-delugeapi",
    version="0.0.1",
    author="Andrew Cole",
    author_email="andrew.cole@illallangi.com",
    description="TODO: SET DESCRIPTION",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/illallangi/DelugeAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['deluge-tool=illallangi.deluge:__main__.cli'],
    },
    install_requires=[
        'beets',
        'click',
        'diskcache',
        'loguru',
        'notifiers',
        'unidecode',
        'yarl',
        'deluge-client==1.3.0',
        'illallangi.btnapi @ git+https://github.com/illallangi/BTNAPI@master',
        'illallangi.orpheusapi @ git+https://github.com/illallangi/OrpheusAPI@master',
        'illallangi.redactedapi @ git+https://github.com/illallangi/RedactedAPI@master',
        'illallangi.torrentapi @ git+https://github.com/illallangi/TorrentAPI@master',
    ]
)
