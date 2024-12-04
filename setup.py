from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.1.15'
DESCRIPTION = 'The Autocorrelation Tools Featured for Time Series actfts package simplifies time series analysis by providing tools for ACF, PACF, and stationarity tests with dynamic, interactive visualizations. It validates and preprocesses data, computes ACF/PACF for multiple lags, and performs tests like Box-Pierce, Ljung-Box, ADF, KPSS, and PP. Results are organized into tables, exportable as TIFF or Excel files, with an interactive mode for on-screen visualization.'
PACKAGE_NAME = 'actfts'
AUTHOR = ['Sergio Andrés Sierra Luján', 'David Esteban Rodríguez Guevara']
EMAIL = ['sergiochess95@gmail.com', 'davestss@hotmail.com']
GITHUB_URL = 'https://sergiofinances.github.io/actfts_python/'
MAINTAINERS = [
    {'name': 'Sergio Andrés Sierra Luján', 'email': 'sergiochess95@gmail.com'}
]

setup(
    name = 'actfts',
    packages = ['actfts'],
    version = VERSION,
    license='MIT',
    description = DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author = AUTHOR,
    author_email = EMAIL,
    url = GITHUB_URL,
    keywords = ['finances', 'econometric', 'time series analysis'],
    install_requires=[
        'requests',
        'numpy',
        'matplotlib',
        'statsmodels',
        'scipy',
        'pandas',
        'Flask>=1.0.0',
        'Werkzeug==2.0.3',
        'plotly',
        'openpyxl',
        'dash',
        'python-dateutil>=2.8.2',
        'pytz>=2020.1',
        'tzdata>=2022.7',
        'patsy>=0.5.6',
        'packaging>=21.3',
        'six>=1.5'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    maintainers=MAINTAINERS
)