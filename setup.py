#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="phtest",
    version="0.0.1",
    description="Платформа тестирования для каведры ФП",
    url="https://github.com/vnetserg/phtest",
    author="Фомин Сергей, Пинянский Андрей",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "Flask-Admin",
        "Flask-BabelEx",
        "Flask-Session",
        "SQLAlchemy"
    ]
)
