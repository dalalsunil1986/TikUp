from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='tikup',
    version='2020.06.10',
    description='An auto downloader and uploader for TikTok videos.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/Coloradohusky/TikUp',
    author='Coloradohusky',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tikup = tikup.tikup:main',
        ],
    },
    python_requires='>=3.5, <4',
    install_requires=['internetarchive>=1.9.3', 'TikTokApi>=3.1.3', 'youtube-dl>=2020.06.06']
)
