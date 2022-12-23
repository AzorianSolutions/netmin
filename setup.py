from setuptools import setup

setup(
    name='netmin',
    version='0.1.0',
    package_dir={'': 'src'},
    install_requires=[
        'click==8.1.3',
        'django==4.1.4',
        'dotenv-cli==3.1.0',
        'jinja2==3.1.2',
        'grapi==0.1.4',
        'pydantic==1.10.2',
        'python-dotenv==0.21.0',
        'requests==2.28.1',
    ],
    entry_points={
        'console_scripts': [
            'netmin = lib.cli.app:cli',
        ],
    },
)
