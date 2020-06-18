# Run kmeans and gmm from scikit-learn to cluster and score crop field data.

import pandas as pd
from sklearn.cluster import KMeans
from sklearn import mixture


def cluster_gmm(data: pd.DataFrame, crop: str, k: int, folder: str):
    """ Compute cluster assignments with optimal BIC score per crop type.
    Method assumes per corp files with latitude and longitude columns
    Produce CSV files with labels and BIC score.
    """
    gmm = mixture.GaussianMixture(n_components=k, covariance_type='full').fit(data)
    bic = gmm.bic(data)
    data['labels'] = gmm.predict(data)
    filename = 'gmm_{}_{:02d}_{:.5f}.csv'.format(crop, k, bic)
    data.to_csv(folder + filename)
    return bic, filename


def cluster_kmeans(data: pd.DataFrame, crop: str, k: int, folder: str):
    kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300,
                    tol=0.00000000000000000000001, algorithm='full').fit(data)
    data['labels'] = kmeans.labels_
    score = kmeans.inertia_
    filename = 'kmeans_{}_{:02d}_{:.5f}.csv'.format(crop, k, score)
    data.to_csv(folder + filename)
    return score, filename


def cluster():
    """For all crops compute, score, and find the best GMM and K-Means clustering."""
    folder = '/Users/N/projects/evapotranspiration/clustering/resources/'
    crops = ['almonds', 'grapes', 'tomatoes', 'pistachios', 'citrus', 'idle']
    for crop in crops:
        data = pd.read_csv(folder + crop + '_clustering.csv')
        data = data[['latitude', 'longitude']]
        best_gmm_k_info = [float('inf'), '']
        best_kmeans_k_info = [float('inf'), '']
        for k in range(2, 20):
            gmm_k_info = cluster_gmm(data, crop, k, folder + 'gmm/')
            if gmm_k_info[0] < best_gmm_k_info[0]:
                best_gmm_k_info = gmm_k_info

            kmeans_k_info = cluster_kmeans(data, crop, k, folder + 'kmeans/')
            if kmeans_k_info[0] < best_kmeans_k_info[0]:
                best_kmeans_k_info = best_kmeans_k_info

        print(best_gmm_k_info[1])
        print(best_kmeans_k_info[1])
