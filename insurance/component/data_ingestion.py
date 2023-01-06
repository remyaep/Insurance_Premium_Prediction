from insurance.entity.config_entity import DataIngestionConfig
import sys,os
from insurance.exception import InsuranceException
from insurance.logger import logging
from insurance.entity.artifact_entity import DataIngestionArtifact
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import shutil

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        """
        
        """
        try:
            logging.info(f"{'>>'*20}Data Ingestion log strated.{'<<'*20} \n\n")
            self.data_ingestion_config = data_ingestion_config
        
        except Exception as e:
            raise InsuranceException(e,sys) from e


    def split_data_as_train_test(self):
        """
        
        """
        try:            
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            download_path = self.data_ingestion_config.dataset_download_path

            os.makedirs(raw_data_dir,exist_ok=True)
            shutil.copy(download_path, raw_data_dir)

            
            file_name = os.listdir(raw_data_dir)[0]
            insurance_file_path = os.path.join(raw_data_dir,file_name)

            logging.info(f"Reading csv file : [{insurance_file_path}]")
            insurance_df = pd.read_csv(insurance_file_path)
            

            insurance_df["expenses_cat"] = pd.cut(insurance_df["expenses"],
                        bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf], labels=[1, 2, 3, 4, 5])

            logging.info(f"Splitting data into train and test")
            split_details = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=132)

            for train_index,test_index in split_details.split(insurance_df, insurance_df["expenses_cat"]):
                start_train_set = insurance_df.loc[train_index].drop(["expenses_cat"],axis=1)
                start_test_set = insurance_df.loc[test_index].drop(["expenses_cat"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            if start_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok= True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                start_train_set.to_csv(train_file_path, index=False)

            if start_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                start_test_set.to_csv(test_file_path,index=False)


            data_ingestion_artifact = DataIngestionArtifact(train_file_path = train_file_path, 
                                    test_file_path = test_file_path,
                                    is_ingested = True,
                                    message = "Data Ingestion completed successfully")

            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact


        except Exception as e:
            raise InsuranceException(e,sys) from e


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        """
        try:
            return self.split_data_as_train_test()
        
        except Exception as e:
            raise InsuranceException(e,sys) from e
    
    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")