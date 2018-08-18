import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doorbell-pi",
    version="0.0.1",
    author="Paul Ridgway",
    author_email="paul@ridgway.io",
    description="An RPi Doorbell service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paul-ridgway/doorbell-pi",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'my_project = doorbell.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)