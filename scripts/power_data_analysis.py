# Methods to prepare power data for analysis
"""
Power data comes in daily files.
Step 1: use parsing_input_files.py to combine them into a single file.
Step 2: create date column out of the given columns (year, month, day).
Step 3: select a year
Step 4: group the data by date by summing all the columns.
    Note that this step will make some other columns invalid.
Step 5: save result as a CSV file.
If not present, set index based on date for plotting. Note: not idempotent.
"""
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


def create_date(data: pd.DataFrame):
    """ Creates date column based on other 3 columns. """
    data['date'] = data[['year', 'month', 'day']].apply(
        lambda x: datetime(x.year, x.month, x.day), axis=1)
    return data


def select_year(data: pd.DataFrame, year: str, date_column='date'):
    """Returns dataframe with only specified year worth of data"""
    data = data[data[date_column] >= str(year)]
    data = data[data[date_column] < str(int(year)+1)]
    data['date'] = data[date_column]
    return data


def filter_irrigation_type(data: pd.DataFrame, power_type: str):
    """Selects only rows with a given irrigation type. """
    return data[data['acctdesc'] == power_type]


def get_total_power_usage(data: pd.DataFrame):
    """Sums the overall daily power consumption. Sets index to 'date'."""
    data = data.groupby(['date']).sum()
    return data


def set_date_as_index(data: pd.DataFrame):
    """Sets index to 'date' column. Used for plotting as timeseries."""
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data = data.set_index('date')
    return data


def get_date_from_datetime(data: pd.DataFrame, column: str):
    """Powwow reports on intervals smaller than hour, use date only."""
    # make sure index has date part only to be able to merge dataframes
    data['date'] = data[[column]].apply(lambda x: pd.to_datetime(x).date(), axis=1)
    return data


def powwow_power_data(folder_path: str):
    """Prepare powwow power files for analysis"""
    # used for: Columbine and Terranova/terranova_power_result.csv
    data = pd.read_csv(folder_path)
    # from start time compute date, removing time, for index alignment
    data = get_date_from_datetime(data, 'Start Time')
    # group by date, aggregate using sum
    #data = get_total_power_usage(data)
    # set index to date
    data = set_date_as_index(data)
    return data


def power_per_crop_per_irrigation_type():
    """Select power data based on power type, year, crop."""
    folder = '/Users/N/projects/evapotranspiration/crop_data/eta-sce'
    crops = ['almonds', 'citrus', 'grapes', 'idle', 'pistachios', 'wheat']
    years = ['2017', '2018', '2019']
    for year in years:
        for crop in crops:
            data = pd.read_csv(folder + '/' + crop + '.csv')
            data = create_date(data)
            data = select_year(data, year)
            data = filter_irrigation_type(data, 'IRRIGATION PUMPING')
            data = get_total_power_usage(data)
            data = set_date_as_index(data)
            data.to_csv(year + '_' + crop + '.csv')
