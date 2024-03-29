import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='quick_sqlite',
    packages=['quick_sqlite'],
    version='1.5',
    license='MIT',
    description='This library can you help you use sqlite3 much easier and faster.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Spark Drago',
    author_email='huzaifa.farooq05@gmail.com',
    url='https://quick-sqlite.readthedocs.io/en/latest/index.html',
    download_url='https://github.com/SparkDrago05/quick_sqlite/',
    keywords=['sqlite', 'sqlite3', 'quick', 'quick_sqlite', 'sqlite3_helper', 'fast_sqlite'],
    install_requires=[
        'cryptography'],
    classifiers=[
        'Development Status :: 4 - Beta',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
    
)
