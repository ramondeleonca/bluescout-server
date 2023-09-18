import pandas as pd
import configparser
import os
from io import StringIO

def parse_csv(csv: str):
    return pd.read_csv(StringIO(csv)).iloc[0].to_dict()

def load_config(default_ini_path: str, config_ini_path: str):
    config = configparser.RawConfigParser(interpolation=configparser.ExtendedInterpolation())
    
    if os.path.exists(default_ini_path):
        config.read(default_ini_path)
        
    if os.path.exists(config_ini_path):
        config.read(config_ini_path)
        
    return config