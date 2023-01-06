from insurance.exception import InsuranceException
from insurance.logger import logging
import os,sys

from insurance.pipeline import Pipeline



def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(e)
        print(e)


if __name__=="__main__":
    main()




    