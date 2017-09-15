from setuptools import setup, find_packages

setup(
    name='simplify-debts',
    version='1.0',
    description='Tool to perform mutual debt simplification',
    url='https://github.com/ric2b/Mutual_Debt_Simplification',
    license='MIT',
    author='',
    author_email='',

    packages=find_packages(exclude=['*.tests']),

    install_requires=['graphviz==0.8'],

    extras_require={
        'test': ['unittest'],
    },

    entry_points={
        'console_scripts': [
            'simplify-debts=mutual_debt.main:main',
        ],
    }
)
