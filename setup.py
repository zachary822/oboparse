import os.path as path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='oboparse',
    version='0.0.1',
    description='OBO file parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Zachary Juang',
    author_email='zacharyjuang+oboparse@gmail.com',
    url='https://github.com/zachary822/oboparse',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['oboparse'],
    python_requires='>=3.6',
    install_requires=['pyparsing'],
    package_data={
        '': ['LICENSE']
    }
)
