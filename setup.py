import json
import os

import setuptools
from setuptools import setup

try:
    import init
    init.initialize_project()
except Exception as e:
    print("Warning: Could not generate protocol buffers:", e)


if os.path.isfile('README.md'):
    with open("README.md", "r") as readme_file:
        long_description = readme_file.read()
else:
    long_description = ''




setup(
    name='sprocket_carball',
    version='1.1.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['pandas', 'protobuf>=5.29.3,<6.0.0',
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
    entry_points={
        'console_scripts': ['carball=carball.command_line:main']
    }
)
