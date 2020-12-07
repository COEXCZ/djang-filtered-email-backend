from setuptools import setup, find_packages

PACKAGE = "django_filtered_email_backend"
NAME = "django-filtered-email-backend"
DESCRIPTION = "Django app for managing email filtering"
AUTHOR = "Pavel Císař - COEX s.r.o (http://www.coex.cz)"
AUTHOR_EMAIL = "pavel.cisar@coex.cz"
URL = "https://github.com/COEXCZ/django-filtered-email-backend"
VERSION = '0.0.1'
LICENSE = "Mozilla Public License 2.0 (MPL 2.0)"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    packages=["django_filtered_email_backend"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Email"
    ],
    install_requires=[
        "django>=2.0.2",
    ],
)
