import setuptools

setuptools.setup(
    name="vigilance",
    version="0.0.1",
    url="https://github.com/MrKriss/vigilance",

    author="Chris Musselle",
    author_email="chris.j.musselle@gmail.com",

    description="A schema definition and validation framework for pandas DataFrames",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=['pandas'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'tox', 'future'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
