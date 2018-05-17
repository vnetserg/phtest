#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="phtest",
    version="0.0.1",
    description="Платформа тестирования для каведры ФП",
    url="https://github.com/vnetserg/phtest",
    author="Фомин Сергей, Пинянский Андрей",
    packages=find_packages(),
    package_data={'phtest': ["static/*", "templates/*"]},
    install_requires=[
        "Flask",
        "Flask-Admin",
        "Flask-BabelEx",
        "Flask-Session",
        "SQLAlchemy"
    ]
)
