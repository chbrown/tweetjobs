from setuptools import setup, find_packages

setup(
    name='tweetjobs',
    version='0.3.11',
    url='http://github.com/chbrown/twilight',
    keywords='twilight oauth crawling bot',
    author='Christopher Brown',
    author_email='io@henrian.com',
    description='Twitter (crawling) tools.',
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: General',
    ],
    install_requires=[
        'psutil',
        'pyshp >= 1.2.0',
        'redis',
        'twython',
    ],
    entry_points={
        'console_scripts': [
            'twilight = twilight.cli.main:main'
        ],
    },
)
