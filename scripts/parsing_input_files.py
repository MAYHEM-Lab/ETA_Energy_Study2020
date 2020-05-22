# Methods to parse multiple input files and create a single DataFrame/CSV file.
from datetime import datetime, timedelta
from glob import glob
from os.path import basename
import pandas as pd


def parse_weekly_filename(filename: str):
    """filename in the example is of the form weekly201801wk4.csv"""
    name = basename(filename)
    return {"year": name[6:10], "month": name[10:12], "week": name[14:15]}


def parse_daily_energy_filename(filename: str):
    """Parse filename string and return dictionary of parameters"""
    # This filename example is of the form /full_path/daily-2016-03-02.csv
    name = basename(filename)
    return {"year": name[6:10], "month": name[11:13], "day": name[14:16]}


def parse_daily_energy_crop_filename(filename: str, crop_name: str):
    """Parse filename string and return dictionary of parameters"""
    # This filename  is of the form /full_path/crop_name-daily-2017-07-16.csv
    filename = basename(filename)
    n = len(crop_name)
    name = filename[n+1:]
    return {"year": name[6:10], "month": name[11:13], "day": name[14:16]}


def parse_daily_eta_filename(filename: str):
    """Parse filename string and return dictionary of parameters"""
    # This filename example is of the form /full_path/CropETa_2019038.csv
    filename = basename(filename)
    year = int(filename[8:12])
    day_of_the_year = int(filename[12:15])
    date = datetime(year, 1, 1) + timedelta(day_of_the_year - 1)
    return {"year": str(year), "month": date.month, "day": date.day}


def flatten_crop_files(folder_path, crops):
    """Flatten CSV files with folder/filename info into a single DataFrame"""
    dataframes = []
    for crop in crops:
        print(crop)
        path = folder_path + "/" + crop + "/*csv"
        filenames = glob(path)
        for filename in filenames:
            params = parse_daily_energy_crop_filename(filename, crop)
            # upload csv data to the datafame
            df = pd.read_csv(filename, index_col=None, header=0)
            # extend dataframe with filename information
            for param in params:
                df[param] = params[param]
            dataframes.append(df)
    frame = pd.concat(dataframes, axis=0, ignore_index=True)
    print('Number of records in the frame: {}'.format(len(frame)))
    return frame


def flatten_files(folder_path):
    """Flatten CSV files with filename info into a single DataFrame"""
    path = folder_path + "/*csv"
    filenames = glob(path)
    dataframes = []
    for filename in filenames:
        params = parse_daily_eta_filename(filename)
        # upload csv data to the datafame
        df = pd.read_csv(filename, index_col=None, header=0)
        # extend dataframe with filename information
        for param in params:
            df[param] = params[param]
        dataframes.append(df)
    frame = pd.concat(dataframes, axis=0, ignore_index=True)
    return frame


def add_date(data):
    data['date'] = data[['year', 'month', 'day']].apply(
        lambda x: datetime(x.year, x.month, x.day), axis=1)


def main():
    # --- 2014 ETa data to a single file --- #
    folder = '/Users/N/projects/evapotranspiration/data/ProcessedETa_2014'
    flatten_files(folder).to_csv(folder + '/2019_eta_census14.csv', sep=';')

    # --- Power per crop data into a single file --- #
    folder = '/Users/N/projects/evapotranspiration/crop_data/eta-sce'
    crops = ['almonds', 'citrus', 'grapes', 'idle','pistachios', 'wheat']
    flatten_crop_files(folder, crops).to_csv(folder + '/all_crops.csv')

    # --- Power per crop data into multiple files --- #
    for crop in crops:
        flatten_crop_files(folder, [crop]).to_csv(folder + '/' + crop + '.csv')

    # --- get number of unique accounts from each dataset --- #
    for crop in crops:
        data = pd.read_csv(folder + '/' + crop + '.csv')
        print(crop, len(data['acct'].unique()))

    # -- preprocess 2016 census ETa file --- #
    folder = '/Users/N/projects/evapotranspiration/data/ProcessedETa_2016'
    flatten_files(folder).to_csv(folder + '/201789_eta_census16.csv', sep=';')


main()
