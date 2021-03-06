from setuptools import setup, find_packages
import ella

install_requires = [
    'setuptools>=0.6b1',
    'Django>=1.8',
    'Pillow<3.0',
    'pytz',
    'django-appdata-mam>=0.1.6',
]

tests_require = [
    'nose',
    'coverage',
    'feedparser',
    'redis',
]

long_description = open('README.rst').read()

setup(
    name='ella',
    version=ella.__versionstr__,
    description='Ella - Django powered CMS',
    long_description=long_description,
    author='Ella Development Team',
    author_email='dev@ella-cms.com',
    license='BSD',
    url='https://github.com/ella/ella',

    packages=find_packages(
        where='.',
        exclude=('doc', 'test_ella', )
    ),

    include_package_data=True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=install_requires,

    test_suite='nose.collector',
    tests_require=tests_require,
)
