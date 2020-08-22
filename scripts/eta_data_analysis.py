# Utility scripts for ETa computation in different formats and measures
from datetime import datetime
import pandas as pd


def daily_eta_acre_inch(data: pd.DataFrame, column='_mean'):
    """
    Formula to compute Acre-Feet from the field size (acres) and mean ETa (")
    Note: if DB column is in inches already, use column parameter as 'inches'.
    Function assumes two columns are present in the data frame.
    :param column:
    :param data: Pandas DataFrame
    :return: Pandas DataFrame
    """
    data['Ac-Ft'] = data['acres'] * data[[column]] / 12.0
    return data


def daily_eta_gallons(data: pd.DataFrame):
    """
    Formula to compute gallons from the field size (acres) and mean ETa (")
    Function assumes two columns are present in the data frame.
    :param data: Pandas DataFrame
    :return: Pandas DataFrame
    """
    gallons_per_acre: int = 27160
    data['gallons'] = data['acres']*data['_mean']*gallons_per_acre
    daily = data.groupby(['date']).sum()
    return daily


def select_year(data: pd.DataFrame, year: str):
    """Return only the part of the dataframe from the given year"""
    # year is given as a 'year' column
    data = data[data['year'] == int(year)]
    return data


def select_year_eta(data: pd.DataFrame, year: str):
    """Return only the part of the dataframe from the given year"""
    # year is part of the 'date' column
    data = data[data['date'] >= str(year)]
    data = data[data['date'] < str(int(year) + 1)]
    return data


def split_into_years(data, folder, years, file_prefix):
    """Split very large dataframe into multiple files for faster analysis."""
    for year in years:
        yearly_data = select_year(data, year)
        yearly_data.to_csv(folder + file_prefix + '_year' + str(year) + '.csv', sep=';')


def create_date(data: pd.DataFrame):
    """Create 'date' column based on three columns: year, month, and day"""
    data['date'] = data[['year', 'month', 'day']].apply(
        lambda x: datetime(x.year, x.month, x.day), axis=1)
    return data


def etl_eta_c_16_data_save_data():
    """Prepare census16 based ETa file for DB import - part 1"""
    # Note: ETa file is couple of gigabytes. use above methods to downsize.
    folder = '../../data/'
    filename = '201789_eta_census16.csv'
    print(folder + filename)
    eta_2016 = pd.read_csv(folder + filename, sep=';')
    years = ['2017', '2018', '2019']
    split_into_years(eta_2016, folder, years, 'eta_2016')


def etl_eta_c_16_data_read_data():
    """Prepare census16 based ETa file for DB import part 2"""
    # Note: ETa file is couple of gigabytes. use above methods to downsize.
    folder = '/../../data/'
    years = ['2017', '2018', '2019']
    for year in years:
        filename = 'eta_census2016_year' + year + '.csv'
        data = pd.read_csv(folder+filename, sep=';')
        # select only necessary columns
        data = data[['OBJECTID_1', 'Acres', 'Crop2016', 'Shape_Area', '_mean', 'year', 'month', 'day']]
        data = create_date(data)
        # Remove other date columns
        data = data[['OBJECTID_1', 'Acres', 'Crop2016', 'Shape_Area', '_mean', 'date']]
        # compute inches based on mean ETa column.
        data['inches'] = data['_mean'] * 0.00539581689
        data.to_csv(folder+year+'eta_census16.csv', index=False, sep=';')


def select_crop(data: pd.DataFrame, crop_column_name: str, crop: str):
    """Select only ETa for the given crop type."""
    data = data[data[crop_column_name] == crop]
    return data


def per_crop_selection():
    folder = '../../data/'
    file = 'eta_c16.csv'
    crops = ['Almonds', 'Citrus', 'Grapes', 'Idle', 'Pistachios', 'Wheat']
    years = ['2017', '2018', '2019']
    data = pd.read_csv(folder + file, sep=';')
    for crop in crops:
        crop_data = select_crop(data, 'crop2016', crop)
        for year in years:
            yearly_crop_data = select_year_eta(crop_data, year)
            yearly_crop_data.to_csv(folder + '/delano_sce_eta_per_crop/' +
                                    'delano_sce_per_crop_' + year + '_' +
                                    crop + '.csv', sep=';', index=False)


def aggregate_eta(data: pd.DataFrame):
    """Sum all the column's values per day."""
    data_daily = data.groupby(['date']).sum()
    return data_daily


def powwow_eta(data: pd.DataFrame):
    """Multiply acres with columns that contain per day ETa and sum."""
    # create pd.Series with those columns
    eta_start_column = 'ETa001'
    eta_end_column = 'ETa365'
    # compute daily eta by selecting ETA columns for all 356 days, and summing inches values for each day
    date_columns = data.columns[data.columns.get_loc(eta_start_column):data.columns.get_loc(eta_end_column)+1]
    for column in date_columns:
        # each column value is multiplied with corresponding field size (acres)
        data[column] = data[column] * data['Acres']/12.0
    result = pd.Series(data[date_columns].sum(), name='Ac-Ft')
    return pd.DataFrame(data[date_columns].sum())
