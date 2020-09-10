from setuptools import setup, find_packages
 
setup(
  name = "meta",
  version = "0.0.2",
  keywords = ["meta"],
  description = "meta core",
  long_description = "meta",
  license = "MIT Licence",
 
  url = "https://github.com/reindexer/meta",
  author = "reindexer",
  author_email = "konglingkai@metatype.cn",

  zip_safe=False, 
  packages = find_packages(exclude=['demo', 'demo.*']),
  include_package_data = True,
  platforms = "any",
  install_requires = ['django', 'Crypto', 'pycrypto'],
)
