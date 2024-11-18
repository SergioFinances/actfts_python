import logging

from actfts.actfts_fun import acfinter

logging.basicConfig(level=logging.INFO)

def main():
    logging.info(acfinter())

if __name__ == '__main__':
    logging.debug('>>> We are starting the execution of the package.')

    main()

    logging.debug('>>> We are finishing the execution of the package.')