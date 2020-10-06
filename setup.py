from setuptools import setup

setup(
    name="blue_interface",
    version="0.0",
    description="Python API for controlling the Blue robot arm",
    url="http://github.com/berkeleyopenarms/blue_interface",
    author="Rachel Thomasson, Brent Yi, Philipp Wu, Greg Balke",
    author_email="brentyi@berkeley.edu",
    license="BSD",
    packages=["blue_interface"],
    install_requires=["ws4py", "PyDispatcher", "numpy", "enum34", "typing"],
    zip_safe=False,
)
