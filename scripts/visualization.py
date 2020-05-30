# Different types of power vs eta visualizations.

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set(context='talk', style='white')

from scripts.eta_data_analysis import daily_eta_acre_inch, aggregate_eta
from scripts.power_data_analysis import get_total_power_usage


def viz_per_crop():
    folder = '/Users/N/projects/evapotranspiration/data/'
    power_folder = folder + 'delano_sce_power_per_crop/'
    eta_folder = folder + 'delano_sce_eta_per_crop/'
    crops = ['almonds', 'citrus', 'grapes', 'idle', 'pistachios', 'wheat']
    years = ['2017', '2018', '2019']
    for crop in crops:
        for year in years:
            # get eta per crop per year
            eta = pd.read_csv(eta_folder + 'delano_sce_per_crop_' +
                              year + '_' + crop + '.csv', sep=';')
            eta['date'] = pd.to_datetime(eta['date'])
            eta = daily_eta_acre_inch(eta)
            daily_eta = aggregate_eta(eta)
            # get power per crop per year
            power = pd.read_csv(power_folder + year + '_' + crop + '.csv')
            daily_power = get_total_power_usage(power)
            # use all_data = daily_eta[0:304] for 2019 - power df is shorter.
            # merge power and eta data into a single dataframe
            all_data = daily_eta
            for c in daily_power.columns:
                all_data[c] = daily_power[c]
                # plot data for different lengths of smoothing windows
            windows = [1, 7, 30]
            for window in windows:
                all_data['ETa (Ac-Ft)'] = all_data['Ac-Ft'].rolling(
                    window=window, min_periods=1).mean()
                all_data['Energy (KWh)'] = all_data['total'].rolling(
                    window=window, min_periods=1).mean()
                all_data.to_csv('delano_sce_c16_per_crop_power_eta_' +
                                year + '_' + crop + '.csv')
                ax = all_data[['ETa (Ac-Ft)', 'Energy (KWh)']].plot(
                    secondary_y=['Energy (KWh)'], figsize=(20, 10))
                ax.set_ylabel('ETa (Ac-Ft)')
                ax.right_ax.set_ylabel('Energy (KWh)')
                plt.title(crop.capitalize() + ' ' + year)
                plt.savefig('delano_sce_c16_per_crop_power_eta_' +
                            year + '_' + crop + str(window) + '.png')
