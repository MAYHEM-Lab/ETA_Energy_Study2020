# Methods to parse multiple input files and create a single DataFrame/CSV file.
from datetime import datetime, timedelta
from glob import glob
from os.path import basename
import pandas as pd

# TODO add filename parsing function as parameter to the flattening function


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


def flatten_files(folder_path: str):
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


def flatten_powwow_power_data(folder_path):
    """Flatten CSV files with into a single DataFrame"""
    # to remove headers first, on mac run: sed -ie "1,14d" filename
    path = folder_path + "/*csv"
    filenames = glob(path)
    dataframes = []
    for filename in filenames:
        # upload csv data to the datafame
        df = pd.read_csv(filename, index_col=None, header=0)
        dataframes.append(df)
    frame = pd.concat(dataframes, axis=0, ignore_index=True)
    return frame


def test_sites_merge():
    folder = '/Users/N/projects/evapotranspiration/PowWow_test_sites/'
    site_folders = ['Columbine_kml/energy_data/', 'Terranova/energy_data/']
    site_results = ['columbine_power_result.csv', 'terranova_power_result.csv']
    for site_folder, site_result in zip(site_folders, site_results):
        result_path = site_folder + site_result
        flatten_powwow_power_data(folder).to_csv(result_path, index=False)


def powwow_2014_census_eta_data_to_single_frame():
    # --- 2014 ETa data to a single file --- #
    # This filename example is of the form /full_path/CropETa_2019038.csv
    # use parse_daily_eta_filename for flattening # TODO
    folder = '/Users/N/projects/evapotranspiration/data/ProcessedETa_2014'
    flatten_files(folder).to_csv(folder + '/2019_eta_census14.csv', sep=';')


def power_per_crop_into_single_file():
    # --- Power per crop data into a single file --- #
    folder = '/Users/N/projects/evapotranspiration/crop_data/eta-sce'
    crops = ['almonds', 'citrus', 'grapes', 'idle','pistachios', 'wheat']
    # TODO
    flatten_crop_files(folder, crops).to_csv(folder + '/all_crops.csv')


def power_per_crop_data_into_multiple_crop_files(folder):
    # --- Power per crop data into multiple files --- #
    folder = '/Users/N/projects/evapotranspiration/crop_data/eta-sce'
    crops = ['almonds', 'citrus', 'grapes', 'idle', 'pistachios', 'wheat']
    for crop in crops:
        flatten_crop_files(folder, [crop]).to_csv(folder + '/' + crop + '.csv')


def number_of_unique_accounts():
    # --- get number of unique accounts from each dataset --- #
    folder = '/Users/N/projects/evapotranspiration/crop_data/eta-sce'
    crops = ['almonds', 'citrus', 'grapes', 'idle', 'pistachios', 'wheat']
    for crop in crops:
        data = pd.read_csv(folder + '/' + crop + '.csv')
        print(crop, len(data['acct'].unique()))


def process_2016_census_eta():
    # -- preprocess 2016 census ETa file --- #
    folder = '/Users/N/projects/evapotranspiration/data/ProcessedETa_2016'
    flatten_files(folder).to_csv(folder + '/201789_eta_census16.csv', sep=';')
