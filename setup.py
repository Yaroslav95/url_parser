#from distutils.core import setup

from setuptools import setup, find_packages

setup(name='url_parser',
      version='0.1',
      description='URL parser',
      classifiers=[
        'Programming Language :: Python :: 3.6',
      ],
      keywords='parser',
      url='https://github.com/yaroslavsapronov/url_parser',
      author='Sapronov Yaroslav',
      author_email='sapr-ya@yandex.ru',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)