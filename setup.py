import json
import os

import setuptools
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


if os.path.isfile('README.md'):
    with open("README.md", "r") as readme_file:
        long_description = readme_file.read()
else:
    long_description = ''


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        from init import initialize_project
        initialize_project()
        # this needs to be last
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        from init import initialize_project
        initialize_project()
        # this needs to be last
        install.run(self)


setup(
    name='sprocket_carball',
    version='0.9.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['pandas', 'protobuf==3.6.1',
                      'openpyxl', 'numpy', 'sprocket-boxcars-py'],
    url='https://github.com/SprocketBot/carball',
    keywords=['rocket-league'],
    license='Apache 2.0',
    author='Sprocket Dev Team',
    author_email='asaxplayinghorse@gmail.com',
    description='Rocket League replay parsing and analysis.',
    long_description=long_description,
    exclude_package_data={
        '': ['.gitignore', '.git/*', '.git/**/*', 'replays/*']},
    long_description_content_type='text/markdown',
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': ['carball=carball.command_line:main']
    }
)
