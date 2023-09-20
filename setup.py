from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in craft_pos/__init__.py
from craft_pos import __version__ as version

setup(
	name="craft_pos",
	version=version,
	description="Extends erpnext pos for bug fixes and additional features\"",
	author="Craft",
	author_email="info@craftinteractive.ae",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
