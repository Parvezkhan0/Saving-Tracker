from setuptools import setup, find_packages

with open("README.md") as readme:
    long_description = readme.read()

with open("requirements.txt") as requirements:
    install_requires = [line.strip() for line in requirements]

setup(
    name="savings_tracker",
    version="0.0.1",
    license="MIT",
    url="https://github.com/Caligatio/savings-tracker",
    author="Brian Turek",
    author_email="brian.turek@gmail.com",
    description="Simple script to help track progress towards savings goals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    entry_points={"console_scripts": ["savings_tracker = savings_tracker:cli"]},
)
