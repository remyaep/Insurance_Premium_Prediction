from cgi import test
from operator import index
from symbol import trailer

from evidently.model_profile import sections
from insurance.constant import DATA_VALIDATION_ARTIFACT
from insurance.entity.config_entity import DataValidationConfig
import sys,os
from insurance.exception import InsuranceException
from insurance.util.util import read_yaml_file
from insurance.logger import logging
from insurance.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
import pandas as pd
import json
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab





class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig, data_ingestion_artifact:DataIngestionArtifact):
        """

        """
        try:
            logging.info(f"{'>>'*20}Data Validation log strated.{'<<'*20} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            
       
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_train_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            return train_df,test_df

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def is_train_test_file_exists(self):
        """
        
        """
        try:

            logging.info("Checking if train and test file exists")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available = is_train_file_exist and is_test_file_exist
            logging.info(f"Is train and test file exists? : {is_available}")

            if not is_available:
                train_file_path = self.data_ingestion_artifact.train_file_path
                test_file_path = self.data_ingestion_artifact.test_file_path

                message = f"Training file : [{train_file_path}] or testing file : [{test_file_path}] is not available"
                
                raise Exception(message)

            return is_available
        
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def validate_dataset_schema(self) -> bool:
        """
        
        """
        try:
            validation_status = False
            schema_file_path = self.data_validation_config.schema_file_path
            schema_info = read_yaml_file(file_path = schema_file_path)
            dataset_columns = list(schema_info["columns"].keys())
            categorical_cols = list(schema_info["categorical_columns"])
            domain_values = schema_info["domain_value"]
            train_df,test_df = self.get_train_test_df()

            train_df_columns = list(train_df.columns)
            test_df_columns = list(test_df.columns)    
              

            column_count_flag = (len(dataset_columns) == len(train_df_columns) and  len(dataset_columns) == len(test_df_columns))
            column_names_flag = dataset_columns.sort() == test_df_columns.sort() and  dataset_columns.sort() == train_df_columns.sort()
            
            if not column_count_flag:
                raise Exception("Column count is not matching")
                
            elif not column_names_flag:
                raise Exception("Column names are not matching")

            else:
                for col in categorical_cols:                   
                    if not (set(train_df[col]).issubset(set(domain_values[col])) and (set(test_df[col]).issubset(set(domain_values[col])))): 
                        raise Exception(f"Categorical values are different for {col}")

            logging.info("Validation passed")
            
            validation_status = True
            
            return validation_status
        
        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_and_save_data_drift_report(self):
        """
        
        """
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df, test_df = self.get_train_test_df() # for now doing with train and test. when new dataset comes, we have to new and old dataset

            profile.calculate(train_df, test_df)
            
            report = json.loads(profile.json())
            
            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)

            os.makedirs(report_dir,exist_ok=True)

            with open(self.data_validation_config.report_file_path, "w") as report_file:
                json.dump(report, report_file, indent= 6)
            
            logging.info(f"JSON Report created at path : [{report_file_path}]")

            return report

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def save_data_dript_report_page(self):
        """
        
        """
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, test_df = self.get_train_test_df()
            dashboard.calculate(train_df, test_df)

            
            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)

            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
            logging.info(f"HTML Report created at path : [{report_page_file_path}]")

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def is_data_drift_found(self) -> bool:
        """
        
        """
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_dript_report_page()
            if (report["data_drift"]["data"]["metrics"]["dataset_drift"]):
                raise Exception("Data drift found")
            
            else:
                logging.info(f"No data drift found")
                return True
        except Exception as e:
            raise InsuranceException(e,sys) from e

    
    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        """
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()


            data_validation_artifact = DataValidationArtifact(schema_file_path = self.data_validation_config.schema_file_path,
            report_file_path = self.data_validation_config.report_file_path,
            report_page_file_path = self.data_validation_config.report_page_file_path,
            is_validated = True,
            message = "Data Validation completed successfully")

            return data_validation_artifact

        except Exception as e:
            raise InsuranceException(e,sys) from e
    
    def __del__(self):
        logging.info(f"{'>>'*20}Data Validation log completed.{'<<'*20} \n\n")
