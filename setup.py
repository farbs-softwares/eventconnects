from setuptools import find_packages, setup

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in eventsconnect/__init__.py
from eventsconnect import __version__ as version

setup(
	name="eventsconnect",
	version=version,
	description="EventsConnect App",
	author="Frappe",
	author_email="school@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
)
