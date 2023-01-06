from insurance.entity.config_entity import DataIngestionConfig,DataTransformationConfig,DataValidationConfig, ModelEvaluationConfig, \
    ModelPusherConfig, ModelTrainerConfig,TrainingPipelineConfig
from insurance.constant import *
from insurance.util.util import read_yaml_file
from insurance.exception import InsuranceException
import sys,os
from insurance.logger import logging


class Configuration:
    def __init__(self,config_file_path:str = CONFIG_FILE_PATH, current_time_stamp:str = CURRENT_TIMESTAMP) -> None :

        try:
            
            self.config_info = read_yaml_file(file_path = config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = CURRENT_TIMESTAMP
            

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Adding configuration for data_ingestion
        """
        try:
            data_ingestion_config_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(artifact_dir,DATA_INGESTION_ARTIFACT,self.time_stamp)

            dataset_download_path = data_ingestion_config_info[DATA_INGESTION_DOWNLOAD_PATH_KEY]
            
            raw_data_dir = os.path.join(data_ingestion_artifact_dir, data_ingestion_config_info[DATA_INGESTION_RAW_DATA_DIR_KEY])

            ingested_dir = os.path.join(data_ingestion_artifact_dir, data_ingestion_config_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY])
            
            ingested_train_dir = os.path.join(ingested_dir, data_ingestion_config_info[DATA_INGESTION_TRAIN_DIR_KEY])
            ingested_test_dir = os.path.join(ingested_dir, data_ingestion_config_info[DATA_INGESTION_TEST_DIR_KEY])

            data_ingestion_config = DataIngestionConfig(dataset_download_path = dataset_download_path,
            raw_data_dir = raw_data_dir,
            ingested_train_dir = ingested_train_dir,
            ingested_test_dir = ingested_test_dir
            )

            logging.info(f"Data Ingestion config: {data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise InsuranceException(e,sys) from e
    

    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Adding configuration for data_ingestion
        """
        try:
            data_validation_config_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            artifact_dir = self.training_pipeline_config.artifact_dir
            data_validation_artifact_dir = os.path.join(artifact_dir,DATA_VALIDATION_ARTIFACT,self.time_stamp)

            schema_file_path = os.path.join(ROOT_DIR, data_validation_config_info[DATA_VALIDATION_SCHEMA_ARTIFACT], data_validation_config_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY])

            report_file_path = os.path.join(data_validation_artifact_dir,data_validation_config_info[DATA_VALIDATION_REPORT_FILE_NAME_KEY])
            report_page_file_path = os.path.join(data_validation_artifact_dir,data_validation_config_info[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY])

            data_validation_config = DataValidationConfig(
                schema_file_path=schema_file_path,
                report_file_path = report_file_path,
                report_page_file_path = report_page_file_path
            )

            logging.info(f"Data Validation config: {data_validation_config}")
            return data_validation_config

        except Exception as e:
            raise InsuranceException(e,sys) from e

    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Adding configuration for data transaformation
        """
        try:
            data_transformation_config_info = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]
            
            artifact_dir = self.get_training_pipeline_config().artifact_dir
            data_transformation_artifact_dir = os.path.join(artifact_dir,DATA_TRANSFORMATION_ARTIFACT,self.time_stamp)

            add_bedroom_per_room = data_transformation_config_info[DATA_TRANSFORMATION_BEDROOM_KEY]

            transformed_dir = os.path.join(data_transformation_artifact_dir,data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY])

            transformed_train_dir = os.path.join(transformed_dir,data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY])
            transformed_test_dir = os.path.join(transformed_dir,data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY])

            preprocessed_dir = os.path.join(data_transformation_artifact_dir,data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY])
            preprocessed_object_file_path = os.path.join(preprocessed_dir,data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY])

            data_transformation_config = DataTransformationConfig(
                add_bedroom_per_room = add_bedroom_per_room,
                transformed_train_dir = transformed_train_dir,
                transformed_test_dir = transformed_test_dir,
                preprocessed_object_file_path = preprocessed_object_file_path
            )

            logging.info(f"Data Transformation config: {data_transformation_config}")
            return data_transformation_config
        except Exception as e:
            raise InsuranceException(e,sys) from e
    
    def get_model_trainer_config(self)->ModelTrainerConfig:
        """
        Adding configuration for model training
        """
        try:
            model_trainer_config_info = self.config_info[MODEL_TRAINER_CONFIG_KEY]
            
            artifact_dir = self.get_training_pipeline_config().artifact_dir
            model_trainer_artifact_dir = os.path.join(artifact_dir,MODEL_TRAINER_ARTIFACT,self.time_stamp)
        
            base_accuracy = model_trainer_config_info[MODEL_TRAINER_BASE_ACCURACY_KEY]
            
            trained_model_file_path = os.path.join(model_trainer_artifact_dir,model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY], \
                model_trainer_config_info[MODEL_TRAINER_MODEL_FILE_NAME_KEY])
            
            model_config_file_path = os.path.join(model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY], \
                model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY])

            model_trainer_config = ModelTrainerConfig(
                trained_model_file_path = trained_model_file_path,
                base_accuracy = base_accuracy,
                model_config_file_path = model_config_file_path
            )

            logging.info(f"Model Trainer config: {model_trainer_config}")
            return model_trainer_config

        except Exception as e:
            raise InsuranceException(e,sys) from e
    
    def get_model_evaluation_config(self) ->ModelEvaluationConfig:
        """
        Adding configuration for model evaluation
        """
        try:
            model_evaluation_config_info = self.config_info[MODEL_EVALUATION_CONFIG_KEY]
            artifact_dir = self.get_training_pipeline_config().artifact_dir
            model_evaluation_artifact_dir = os.path.join(artifact_dir,MODEL_EVALUATION_ARTIFACT_DIR) # timestamp not required here as we are comparing eith best model

            model_evaluation_file_path = os.path.join(model_evaluation_artifact_dir,model_evaluation_config_info[MODEL_EVALUATION_FILE_NAME_KEY])
            
            model_evaluation_config = ModelEvaluationConfig(
                model_evaluation_file_path = model_evaluation_file_path,
                time_stamp = self.time_stamp
            )

            logging.info(f"Model Evaluation config: {model_evaluation_config}")
            return model_evaluation_config

        except Exception as e:
            raise InsuranceException(e,sys) from e
    
    def get_model_pusher_config(self) ->ModelPusherConfig:
        """
        Adding configuration for model pushing
        """
        try:
            model_pusher_config_info = self.config_info[MODEL_PUSHER_CONFIG_KEY]
            
            export_dir_path = os.path.join(ROOT_DIR,model_pusher_config_info[MODEL_PUSHER_EXPORT_DIR_KEY],self.time_stamp)

            model_pusher_config = ModelPusherConfig(
                export_dir_path
            )

            logging.info(f"Model Evaluation config: {model_pusher_config}")
            return model_pusher_config

        except Exception as e:
            raise InsuranceException(e,sys) from e
    
    def get_training_pipeline_config(self) ->TrainingPipelineConfig:
        try:
            
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY], training_pipeline_config[TRAINING_PIPELINE_ARIFACT_DIR_KEY]
            )
            
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=str(artifact_dir))
            logging.info(f"Training pipleine config: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise InsuranceException(e,sys) from e
