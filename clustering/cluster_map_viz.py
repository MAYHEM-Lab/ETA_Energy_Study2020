# Create dynamic HTML maps from CSVs with clustering assignment lat/long/label.

from glob import glob
import matplotlib.pyplot as plt
import mplleaflet
from os import path
import pandas as pd
import seaborn as sns

sns.set(context='talk', style='white')


def generic_plot(file: str, title: str, out_file: str):
    """Creates a dynamic HTML map from the lat/lon and labels columns."""
    data = pd.read_csv(file)
    fig = plt.figure(figsize=(20, 20))
    plt.scatter(data.longitude, data.latitude, cmap=plt.cm.brg, c=data.labels, s=10)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(title)
    plt.tight_layout()
    mplleaflet.show(fig, path=out_file)


def plot_all(folders):
    """Creates a map for each one of the CSV files."""
    for folder in folders:
        files = glob(folder + "*csv")
        for file in files:
            title = path.basename(file).split('.csv')[0]
            generic_plot(file, title, out_file=folder + title + '.html')


def plot_field_centers_dynamic_html(folder: str, file: str):
    method, crop, k = path.basename(file).split('.')[0].split('_')
    title = '{} K={} {}'.format(crop, k, method)
    out_file = folder + '{}_{}_{}.html'.format(method, crop, k)
    generic_plot(file, title, out_file)


def plot_all_crops(folders):
    """Creates a map for each one of the crop labeled CSV files."""
    for folder in folders:
        files = glob(folder + "*csv")
        for file in files:
            plot_field_centers_dynamic_html(folder, file)
