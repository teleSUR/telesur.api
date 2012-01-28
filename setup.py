from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='telesur.api',
      version=version,
      description="API para interactuar con Plone y el sitio Web Multimedia teleSUR",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Plone :: 4.1",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        ],
      keywords='Plone CMS API website teleSUR rest',
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
          # collective.nitf especifica las dependencias de dexterity
          # las cuales incluyen five.grok y plone.app.z3cform, entre otras.
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
