import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns



sns.set(context='talk', style='white')

# data: pd.DataFrame, labels: list
def plot_field_centers():
    fig = plt.figure(figsize=(20, 20))
    map_img = plt.imread('/Users/N/projects/evapotranspiration/ETA_Energy_Study2020/resources/delano.png')
    data = pd.read_csv('/Users/N/projects/evapotranspiration/ETA_Energy_Study2020/resources/almonds_clustering.csv')


    #plt.subplot(2, 3, placement[covar_type][covar_tied])
    plt.scatter(data.longitude, data.latitude, c=data.labels, s=10)

    bbox = (data.longitude.min(), data.longitude.max(),
             data.latitude.min(), data.latitude.max())
    plt.scatter(data.longitude, data.latitude, c=data.labels, cmap=plt.cm.brg, s=10)
    plt.imshow(map_img, zorder=0, extent=bbox, aspect= 'equal')
    plt.xlim(left=bbox[0], right=bbox[1])
    plt.ylim(bottom=bbox[2], top=bbox[3])
    plt.xticks([])
    plt.yticks([])
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Full-Tied: K={}'.format(3))
    plt.tight_layout()
    plt.savefig('test.png')
    return fig

# gmm_almonds_3_-14272.547215979122.csv
def plot_gmms():
    #for k in range(2, 11):
    plt.clf()
    #crop = 'Almonds'
    crop = 'Almonds'
    # best_bic = [['Almonds', 3, 'gmm_almonds_03_-14274.59189.csv'],
    #             ['Citrus', 7, 'gmm_citrus_07_-13701.18274.csv'],
    #             ['Grapes', 6, 'gmm_grapes_06_-27952.51934.csv'],
    #             ['Idle', 4, 'gmm_idle_04_-6312.08513.csv'],
    #             ['Pistachios', 5, 'gmm_pistachios_05_-7591.92575.csv'],
    #             ['Tomatoes', 3, 'gmm_tomatoes_03_-3319.00625.csv']]

    # kmeans_best_bic = [ hypatia
    #     ['Almonds', 2,'best_bic_kmeans_almonds_2.csv'],
    #  ['Citrus', 7, 'best_bic_kmeans_citrus_7.csv'],
    #  ['Grapes', 4, 'best_bic_kmeans_grapes_4.csv'],
    #  ['Idle', 3, 'best_bic_kmeans_idle_3.csv'],
    #  ['Pistachios',3, 'best_bic_kmeans_pistachios_3.csv'],
    #  ['Tomatoes', 3,'best_bic_kmeans_tomatoes_3.csv']]

    kmeans_best_bic = [
        ['Almonds', 5, 'kmeans_almonds_05_2.15991.csv'],
        ['Citrus', 5, 'kmeans_citrus_05_0.80928.csv'],
        ['Grapes', 5, 'kmeans_grapes_05_3.28978.csv'],
        ['Idle', 5, 'kmeans_idle_05_1.01457.csv'],
        ['Pistachios', 5, 'kmeans_pistachios_05_0.96093.csv'],
        ['Tomatoes', 5, 'kmeans_tomatoes_05_0.13918.csv']]

    for crop, k, filename in kmeans_best_bic:

        # data = pd.read_csv('/Users/N/projects/evapotranspiration/ETA_Energy_Study2020/scripts/gmm_{}.csv'.format(k))
        data = pd.read_csv('/Users/N/projects/evapotranspiration/ETA_Energy_Study2020/resources/kmeans/kmeans/'+filename)
        fig = plt.figure(figsize=(20, 20))

        map_img = plt.imread('/Users/N/projects/evapotranspiration/ETA_Energy_Study2020/resources/delano.png')

        plt.scatter(data.longitude, data.latitude, c=data.labels, s=10)

        bbox = (data.longitude.min(), data.longitude.max(),
                data.latitude.min(), data.latitude.max())
        plt.scatter(data.longitude, data.latitude, c=data.labels, cmap=plt.cm.brg, s=10)
        plt.imshow(map_img, zorder=0, extent=bbox, aspect='equal')
        plt.xlim(left=bbox[0], right=bbox[1])
        plt.ylim(bottom=bbox[2], top=bbox[3])
        plt.xticks([])
        plt.yticks([])
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('{} K={} (kmeans-scikit)'.format(crop, k))
        plt.tight_layout()
        plt.savefig('./scikit_kmeans/best_bic_kmeans-sl_{}_{}.png'.format(crop, k))



def main():
    print("test")
    #plot_field_centers()
    plot_gmms()

main()