from setuptools import setup, find_packages

setup(
    name='servent',
    version='0.0.1',
    description='a servent to help you',

    author='bravomikekilo',
    author_email='bravomikekilo@outlook.com',

    keywords='helper machine-learning',

    packages=find_packages(exclude=['tests', 'docs']),
    scripts=['scripts/servent'],

    extras_require={
        'test': ['nose>=1.0']
    }

)


