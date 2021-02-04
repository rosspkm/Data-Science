import os
import re
import pandas
import time
import statistics
from pandas import DataFrame
from datetime import datetime

class MVTSSample:
    
    def __init__(self, flare_type:str, start_time:datetime, end_time:datetime, data:DataFrame):
        self._flare_type = flare_type
        self._start_time = start_time
        self._end_time = end_time
        self._data = data
    
    def get_flare_type(self):
        return self._flare_type
    
    def get_start_time(self):
        return self._start_time
    
    def get_end_time(self):
        return self._end_time
    
    def get_data(self):
        return self._data

def read_flare_mvts(data_dir:str, file_name:str) -> MVTSSample:
    return MVTSSample(file_name[0], re.search('_s(.+?)_e', file_name).group(1),
    re.search('_e(.+?).csv', file_name).group(1), pandas.read_csv(f'{data_dir}/{file_name}', sep='\t'))

def read_non_flare_mvts(data_dir:str, file_name:str) -> MVTSSample:
    return MVTSSample(file_name[:2] if file_name.startswith("F") else file_name[0], 
    re.search('_s(.+?)_e', file_name).group(1), re.search('_e(.+?).csv', file_name).group(1), pandas.read_csv(f'{data_dir}/{file_name}', sep='\t'))

def calculate_descriptive_features(data:DataFrame)-> DataFrame:
    variates_to_calc_on = [ 'R_VALUE','TOTUSJH','TOTBSQ','TOTPOT','TOTUSJZ','ABSNJZH','SAVNCPP',
                           'USFLUX','TOTFZ','MEANPOT','EPSZ','MEANSHR','SHRGT45','MEANGAM','MEANGBT',
                           'MEANGBZ','MEANGBH','MEANJZH','TOTFY','MEANJZD','MEANALP','TOTFX']
    features_to_return = [ 'R_VALUE_MEAN','R_VALUE_STDDEV',
                          'TOTUSJH_MEAN','TOTUSJH_STDDEV',
                          'TOTBSQ_MEAN','TOTBSQ_STDDEV',
                          'TOTPOT_MEAN','TOTPOT_STDDEV',
                          'TOTUSJZ_MEAN','TOTUSJZ_STDDEV',
                          'ABSNJZH_MEAN','ABSNJZH_STDDEV',
                          'SAVNCPP_MEAN','SAVNCPP_STDDEV',
                          'USFLUX_MEAN','USFLUX_STDDEV',
                          'TOTFZ_MEAN','TOTFZ_STDDEV',
                          'MEANPOT_MEAN','MEANPOT_STDDEV',
                          'EPSZ_MEAN','EPSZ_STDDEV',
                          'MEANSHR_MEAN','MEANSHR_STDDEV',
                          'SHRGT45_MEAN','SHRGT45_STDDEV',
                          'MEANGAM_MEAN','MEANGAM_STDDEV',
                          'MEANGBT_MEAN','MEANGBT_STDDEV',
                          'MEANGBZ_MEAN','MEANGBZ_STDDEV',
                          'MEANGBH_MEAN','MEANGBH_STDDEV',
                          'MEANJZH_MEAN','MEANJZH_STDDEV',
                          'TOTFY_MEAN','TOTFY_STDDEV',
                          'MEANJZD_MEAN','MEANJZD_STDDEV',
                          'MEANALP_MEAN','MEANALP_STDDEV',
                          'TOTFX_MEAN','TOTFX_STDDEV']
    temp_list = []
    df = pandas.DataFrame(data)
    for i in variates_to_calc_on:
        temp_list.append(statistics.mean(df[i].tolist()))
        temp_list.append(statistics.stdev(df[i].tolist()))

    return pandas.DataFrame(data={k:[v] for k,v in zip(features_to_return, temp_list)})

def process_partition(partition_location:str, abt_name:str):
    abt_header = [ 'FLARE_TYPE', 'R_VALUE_MEAN','R_VALUE_STDDEV',
                          'TOTUSJH_MEAN','TOTUSJH_STDDEV',
                          'TOTBSQ_MEAN','TOTBSQ_STDDEV',
                          'TOTPOT_MEAN','TOTPOT_STDDEV',
                          'TOTUSJZ_MEAN','TOTUSJZ_STDDEV',
                          'ABSNJZH_MEAN','ABSNJZH_STDDEV',
                          'SAVNCPP_MEAN','SAVNCPP_STDDEV',
                          'USFLUX_MEAN','USFLUX_STDDEV',
                          'TOTFZ_MEAN','TOTFZ_STDDEV',
                          'MEANPOT_MEAN','MEANPOT_STDDEV',
                          'EPSZ_MEAN','EPSZ_STDDEV',
                          'MEANSHR_MEAN','MEANSHR_STDDEV',
                          'SHRGT45_MEAN','SHRGT45_STDDEV',
                          'MEANGAM_MEAN','MEANGAM_STDDEV',
                          'MEANGBT_MEAN','MEANGBT_STDDEV',
                          'MEANGBZ_MEAN','MEANGBZ_STDDEV',
                          'MEANGBH_MEAN','MEANGBH_STDDEV',
                          'MEANJZH_MEAN','MEANJZH_STDDEV',
                          'TOTFY_MEAN','TOTFY_STDDEV',
                          'MEANJZD_MEAN','MEANJZD_STDDEV',
                          'MEANALP_MEAN','MEANALP_STDDEV',
                          'TOTFX_MEAN','TOTFX_STDDEV']

    data_dir1 = "C:/Users/User/Desktop/python class/data/partition1/FL"
    data_dir2 = "C:/Users/User/Desktop/python class/data/partition1/NF"
    analyzed = []

    for file_name in os.listdir(data_dir1):
        try:
            results = read_flare_mvts(data_dir1, file_name)
            data = calculate_descriptive_features(results.get_data())
            data.insert(0, 'FLARE_TYPE', results.get_flare_type())
            analyzed.append(data)
        except:
            print(f'{file_name} was passed')
            continue
    
    for file_name in os.listdir(data_dir2):
        try:
            results = read_non_flare_mvts(data_dir2, file_name)
            data = calculate_descriptive_features(results.get_data())
            data.insert(0, 'FLARE_TYPE', results.get_flare_type())
            analyzed.append(data)
        except:
            print(f'{file_name} was passed')
            continue

    
    df = pandas.concat(analyzed)
    df.to_csv(f'{partition_location}/{abt_name}.csv', sep="\t", index =False, header=True)

    
start = time.time()                       
data_dir = "C:/Users/User/Desktop/python class/data/partition1"
process_partition(data_dir, "Flare-Analyzed-Data")
end = time.time()
print(end-start)