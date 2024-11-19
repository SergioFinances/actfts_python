import logging

import pandas as pd
from actfts.actfts_fun import acfinter
from actfts.Datasets import DPIEEUU_dataset
from actfts.Datasets import GDPEEUU_dataset
from actfts.Datasets import PCECEEUU_dataset

logging.basicConfig(level=logging.INFO)

def main():
    datag = DPIEEUU_dataset()
    x = datag['DPIEEUU']
    logging.info(acfinter(datag = x))
    logging.info(DPIEEUU_dataset())
    logging.info(GDPEEUU_dataset())
    logging.info(PCECEEUU_dataset())

if __name__ == '__main__':
    logging.debug('>>> We are starting the execution of the package.')

    main()

    logging.debug('>>> We are finishing the execution of the package.')