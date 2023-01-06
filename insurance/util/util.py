import yaml
from insurance.exception import InsuranceException
import os,sys
import numpy as np
import dill
import pandas as pd
from insurance.constant import *



def read_yaml_file(file_path) -> dict:
    """
    Reads the YAML file and returns the content as a dictionary
    """
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
            
    except Exception as e:
        raise InsuranceException(e,sys) from e

def write_yaml_file(file_path:str, data:dict = None):

    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                return yaml.dump(data, yaml_file)
    
    except Exception as e:
        raise InsuranceException(e,sys)

def save_numpy_array_data(file_path:str, array:np.array):
    """
    Save numpy array data to file
    """
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise InsuranceException(e,sys) from e


def load_numpy_array_data(file_path:str):
    """
    Load numpy array data to file
    """
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise InsuranceException(e,sys) from e

def save_object(file_path:str,obj):
    """
    """
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,"wb")as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise InsuranceException(e,sys) from e

def load_object(file_path:str):
    """
    """
    try:
       with open(file_path,"rb")as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise InsuranceException(e,sys) from e

def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
    try:
        datatset_schema = read_yaml_file(schema_file_path)

        schema = datatset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        dataframe = pd.read_csv(file_path)

        error_messgae = ""


        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_messgae = f"{error_messgae} \nColumn: [{column}] is not in the schema."
        if len(error_messgae) > 0:
            raise Exception(error_messgae)
        return dataframe

    except Exception as e:
        raise InsuranceException(e,sys) from e

