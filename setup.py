from distutils.core import setup
setup(
    name='sqlite_easy',
    packages=['sqlite_easy'],
    version='0.1',
    license='MIT',
    description='This library can you help you use sqlite3 much easier and faster.',
    author='Spark Drago',
    author_email='huzaifa.farooq05@gmail.com',
    url='https://github.com/SparkDrago05/sqlite_easy',
    download_url='https://github.com/SparkDrago05/sqlite_easy/archive/v_01.tar.gz',
    keywords=['sqlite', 'sqlite3'],
    install_requires=[
        'validators',
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
