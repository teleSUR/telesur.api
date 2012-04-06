# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='telesur.api',
      version=version,
      description="API para interactuar con Plone y el sitio web Video teleSUR",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone api teleSUR rest',
      author='Joaquin Rosales',
      author_email='globojorro@gmail.com',
      url='https://github.com/desarrollotv/telesur.api',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['telesur'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'collective.nitf',
        'plone.behavior',
        'plone.directives.form',
        'rwproperty',
        ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
