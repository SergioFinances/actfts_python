from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.1.0'
DESCRIPTION = 'The Autocorrelation Tools Featured for Time Series actfts package simplifies time series analysis by providing tools for ACF, PACF, and stationarity tests with dynamic, interactive visualizations. It validates and preprocesses data, computes ACF/PACF for multiple lags, and performs tests like Box-Pierce, Ljung-Box, ADF, KPSS, and PP. Results are organized into tables, exportable as TIFF or Excel files, with an interactive mode for on-screen visualization.'
PACKAGE_NAME = 'actfts'
AUTHOR = ['Sergio Andrés Sierra Luján', 'David Esteban Rodríguez Guevara']
EMAIL = ['sergiochess95@gmail.com', 'davestss@hotmail.com']
GITHUB_URL = 'https://sergiofinances.github.io/actfts/'
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
        'requests>=2.20.0',
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'arch>=4.0',
        'matplotlib>=3.3.0',
        'statsmodels>=0.12.0',
        'lxml_html_clean>=0.4.0',
        'xlrd>=2.0.1',
        'dash>=2.0.0',
        'openpyxl>=3.0.0',
        'pathlib; python_version<"3.4"'
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