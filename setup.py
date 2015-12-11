from distutils.core import setup

setup(
    name='taxi_api',
    version='0.1',
    packages=['taxi_api', 'taxi_api/resources'],
    package_dir={'taxi_api': 'taxi_api'},
    license='LuizCapu All rights reserved',
    long_description=open('README.md').read(),
)
