import setuptools

setuptools.setup(
    name="vigilance",
    version="0.1",
    url="https://github.com/MrKriss/vigilance",

    author="Chris Musselle",
    author_email="chris.j.musselle@gmail.com",

    description="A simple data validation approach for testing assumptions about pandas DataFrames in Python.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=['pandas', 'decorator', 'future', 'astor'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'future'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
