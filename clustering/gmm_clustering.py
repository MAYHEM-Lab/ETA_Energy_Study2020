# Run kmeans and gmm from scikit-learn to cluster and score crop field data.

import pandas as pd
from sklearn.cluster import KMeans
from sklearn import mixture


def cluster_gmm(data: pd.DataFrame, columns: [str], crop: str, k: int, folder: str, region: str):
    """ Compute cluster assignments with optimal BIC score per crop type.
    Method assumes per corp files with latitude and longitude columns
    Produce CSV files with labels and BIC score.
    """
    gmm = mixture.GaussianMixture(n_components=k, covariance_type='full').fit(data[columns])
    bic = gmm.bic(data)
    data_to_save = data.copy(deep=True)
    labels = gmm.predict(data)
    data_to_save['labels'] = labels
    filename = 'gmm_{}_{}_{:02d}_{:.5f}.csv'.format(region, crop, k, bic)
    data_to_save.to_csv(folder + filename)
    return bic, labels


def cluster_kmeans(data: pd.DataFrame, crop: str, k: int, folder: str):
    kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300,
                    tol=0.00000000000000000000001, algorithm='full').fit(data)
    data['labels'] = kmeans.labels_
    score = kmeans.inertia_
    filename = 'kmeans_{}_{:02d}_{:.5f}.csv'.format(crop, k, score)
    data.to_csv(folder + filename)


def cluster(folder, crops, columns, region):
    """For all crops compute, score, and find the best GMM and K-Means clustering."""
    for crop in crops:
        data = pd.read_csv(folder + crop + '_clustering.csv')
        data = data[['latitude', 'longitude']]
        for k in range(2, 21):
            gmm_score, _ = cluster_gmm(data, columns, crop, k, folder + 'gmm/', region)
            cluster_kmeans(data, crop, k, folder + 'kmeans/')


def cluster_wtd(folder, crops, regions, ext='_wt.csv'):
    """Clustering of per region per crop fields based on
    their latitude, longitude and depth of the water table."""
    columns = ['latitude', 'longitude', '_mean']
    for region in regions:
        for crop in crops:
            filename = crop + '_' + region + ext
            data = pd.read_csv(folder + filename)
            data_to_fit = data.copy(deep=True)
            data_to_fit = data_to_fit[columns]
            best_gmm_score = float('inf')
            best_gmm_k = 0
            k = 0
            try:
                for k in range(1, 11):
                    # GMM
                    gmm_score, _ = cluster_gmm(data_to_fit, columns,
                                               crop, k, folder + 'results/gmm_wt_ll/csv/', region)
                    if gmm_score < best_gmm_score:
                        best_gmm_score = gmm_score
                        best_gmm_k = k
                    # K-means
                    cluster_kmeans(data_to_fit, crop, k, folder + 'results/kmeans_wt/csv/')
            except Exception as e:
                print(e)
                print(crop + str(k))
            print(crop + str(best_gmm_k))


def cluster_gmm_cli(data: pd.DataFrame, crop: str, k: int, folder: str):
    """ Compute cluster assignments with optimal BIC score per crop type.
    Method assumes per corp files with latitude and longitude columns
    Produce CSV files with labels and BIC score.
    """

    try:
        gmm = mixture.GaussianMixture(n_components=k, covariance_type='full').fit(data)
        bic = gmm.bic(data)
        labels = gmm.predict(data)
        return bic, labels
    except:
        print(crop + str(k))


def cluster_all_data_llw():
    folder = '.../wtd/'
    crops = ['almonds', 'almonds', 'citrus', 'citrus', 'grapes', 'grapes',
             'idle', 'idle', 'pistachios', 'pistachios', 'tomatoes', 'tomatoes']
    regions = ['fresno', 'kern']
    cluster_wtd(folder, crops, regions)
