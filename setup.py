from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="blue_interface",
    version="0.1",
    description="Python API for controlling the Blue robot arm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/berkeleyopenarms/blue_interface",
    author="Rachel Thomasson, Brent Yi, Philipp Wu, Greg Balke",
    author_email="brentyi@berkeley.edu",
    license="BSD",
    packages=["blue_interface"],
    install_requires=["ws4py", "PyDispatcher", "numpy", "enum34", "typing"],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
