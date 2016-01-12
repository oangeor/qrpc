from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='qrpc',

    version='0.1.0',

    description='A Python RPC Framework',
    long_description=long_description,

    url='https://github.com/oangeor/qrpc',

    author='chuncheng',
    author_email='ischuncheng@gmail.com',

    license='MIT',

    classifiers=[

        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
    ],

    keywords='rpc',

    packages=['qrpc', 'qrpc.middleware'],

    install_requires=[
        'requests>=2.18.4',
        'six>=1.10.0',
        'falcon>=1.2.0',
    ],

)
