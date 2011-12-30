from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='telesur.api',
      version=version,
      description="API para Plone CMS de TeleSUR",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Plone API',
      author='Joaquin Rosales',
      author_email='globojorro@gmail.com',
      url='http://svn.plone.org/svn/collective/',
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
      ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
