# Different types of power vs eta visualizations.

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import scripts.eta_data_analysis as ea
import scripts.power_data_analysis as pa

sns.set(context='talk', style='white')


def viz_per_crop():
    """Visualize per crop ETa vs power for Delano-SCE region."""
    folder = '../../data/'
    # see power_data_analysis.py for more details
    power_folder = folder + 'delano_sce_power_per_crop/'
    # see eta_data_analysis.py for more details
    eta_folder = folder + 'delano_sce_eta_per_crop/'
    crops = ['almonds', 'citrus', 'grapes', 'idle', 'pistachios', 'wheat']
    years = ['2017', '2018', '2019']
    for crop in crops:
        for year in years:
            # get eta per crop per year
            eta = pd.read_csv(eta_folder + 'delano_sce_per_crop_' + year + '_' + crop + '.csv', sep=';')
            eta['date'] = pd.to_datetime(eta['date'])
            eta = ea.daily_eta_acre_inch(eta)
            daily_eta = ea.aggregate_eta(eta)
            # get power per crop per year
            power = pd.read_csv(power_folder + year + '_' + crop + '.csv')
            daily_power = pa.get_total_power_usage(power)
            # use all_data = daily_eta[0:304] for 2019 - power df is shorter.
            # merge power and eta data into a single DataFrame
            all_data = daily_eta
            for c in daily_power.columns:
                all_data[c] = daily_power[c]
                # plot data for different lengths of smoothing windows
            windows = [1, 7, 30]
            for window in windows:
                all_data['ETa (Ac-Ft)'] = all_data['Ac-Ft'].rolling(window=window, min_periods=1).mean()
                all_data['Energy (KWh)'] = all_data['total'].rolling(window=window, min_periods=1).mean()
                all_data.to_csv('delano_sce_c16_per_crop_power_eta_' + year + '_' + crop + '.csv')
                ax = all_data[['ETa (Ac-Ft)', 'Energy (KWh)']].plot(
                    secondary_y=['Energy (KWh)'], figsize=(20, 10))
                ax.set_ylabel('ETa (Ac-Ft)')
                ax.right_ax.set_ylabel('Energy (KWh)')
                plt.title(crop.capitalize() + ' ' + year)
                plt.savefig('delano_sce_c16_per_crop_power_eta_' +
                            year + '_' + crop + str(window) + '.png')


def plot_power_per_crop_per_irrigation_type():
    """Plots power only graphs per crop and irrigation type."""
    # data produced by pa.power_per_crop_per_irrigation_type
    crops = ['almonds', 'citrus', 'grapes', 'idle', 'pistachios', 'wheat']
    years = ['2017', '2018', '2019']
    windows = [1, 7, 30]
    for year in years:
        for crop in crops:
            data = pd.read_csv('crop_csv/' + year + '_' + crop + '.csv')
            place = 'delano_sce'
            for window in windows:
                data['Energy (KWh)'] = data['total'].rolling(
                    window=window, min_periods=1).mean()
                data[['Energy (KWh)']].plot(figsize=(20, 10))
                plt.title(crop)
                plt.savefig('images/crop/power_' + place + '_' + str(year)
                            + '_' + crop + '_' + str(window) + '.png')


def terranova_prepare():
    """Prepare DataFrame with Power and ETa columns for Terranova."""
    folder = '../../PowWow_test_sites/Terranova/'
    power_file = 'terranova_power_result.csv'
    power = pd.read_csv(folder + power_file)
    years = ['2017', '2018', '2019']
    for year in years:
        yearly_eta = ea.powwow_eta(pd.read_csv(folder + 'ETa/terranova_daily_' + year + '_inches.csv'))
        yearly_eta.to_csv(folder + 'daily_eta' + year + '.csv')  # Note: header
        daily_eta = pd.read_csv(folder + 'daily_eta' + year + '.csv')
        # # already aggregated
        yearly_power = pa.select_year(power, year, 'Start Time')
        daily_power = pa.get_total_power_usage(yearly_power)
        daily_power.to_csv(folder + 'daily_power_' + year + '.csv')
        daily_power = pd.read_csv(folder + 'daily_power_' + year + '.csv')
        all_data = daily_power
        all_data['Ac-FT'] = daily_eta['eta']
        all_data.to_csv(folder + 'terranova_eta_power_' + year + '.csv')


def columbine_prepare():
    """Prepare DataFrame with Power and ETa columns for Columbine."""
    # Note: different formats in which farm ETa files come.
    folder = '../../PowWow_test_sites/Columbine_kml/'
    power = pd.read_csv(folder + 'columbine_power_result.csv')
    eta = pd.read_csv(folder + 'eta_columbine_c16.csv', sep=';')
    years = ['2017', '2018', '2019']
    for year in years:
        yearly_eta = ea.select_year_eta(eta, year)
        yearly_eta = ea.daily_eta_acre_inch(yearly_eta, column='inches')
        daily_eta = ea.aggregate_eta(yearly_eta)
        yearly_power = pa.select_year(power, year, 'Start Time')
        daily_power = pa.get_total_power_usage(yearly_power)
        print(daily_power.head())
        all_data = daily_eta
        for c in daily_power.columns:
            all_data[c] = daily_power[c]
        all_data.to_csv(folder + 'columbine_eta_power_' + year + '.csv')


def plot_prepared_test_site(folder: str, years: [str], site: str, windows=(1, 7, 30)):
    for year in years:
        filename = folder + site + '_eta_power_' + year + '.csv'
        all_data = pd.read_csv(filename)
        for window in windows:
            all_data['ETa (Ac-Ft)'] = all_data['eta'].rolling(window=window, min_periods=1).mean()
            all_data['Energy (KWh)'] = all_data['Consumed (kWH)'].rolling(window=window, min_periods=1).mean()
            ax = all_data[['ETa (Ac-Ft)', 'Energy (KWh)']].plot(secondary_y=['Energy (KWh)'], figsize=(20, 10))
            ax.set_ylabel('ETa (Ac-Ft)')
            ax.right_ax.set_ylabel('Energy (KWh)')
            plt.title(site.capitalize() + ' ' + year)
            plt.savefig(site + '_power_eta_' + year + '_' + str(window) + '.png')


def plot_test_sites():
    folder = '../../PowWow_test_sites/'
    params = [[folder + 'Columbine_kml/', ['2018', '2019'], 'columbine'],
              [folder + 'Terranova/', ['2017', '2018', '2019'], 'terranova']]
    for param in params:
        plot_prepared_test_site(param[0], param[1], param[2])


def plot_power_per_crop_per_cluster_per_irrigation_type():
    """Plots power only graphs per crop and irrigation type."""
    # data produced by pa.power_per_crop_per_irrigation_type
    folder = '../../crop_clusters/'
    # crops = ['almonds', 'citrus', 'grapes', 'idle', 'pistachios', 'wheat']
    crops = ['almonds0', 'almonds1', 'almonds2']
    years = ['2017', '2018', '2019']
    windows = [1, 7, 30]
    for year in years:
        for crop in crops:
            data = pd.read_csv(folder + year + '_' + crop + '.csv')
            place = 'delano_sce'
            for window in windows:
                data['Energy (KWh)'] = data['total'].rolling(
                    window=window, min_periods=1).mean()
                data[['Energy (KWh)']].plot(figsize=(20, 10))
                plt.title(crop)
                plt.savefig(folder + 'images/power_' + place + '_' + str(year)
                            + '_' + crop + '_' + str(window) + '.png')
