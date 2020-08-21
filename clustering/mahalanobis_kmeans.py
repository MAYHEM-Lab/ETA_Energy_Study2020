# Cluster crop fields, score, and filter for minimum cluster size.

from clustering import sf_kmeans
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn import preprocessing


def run_kmeans(k: int, n_init: int, filename: str, columns: [str]):
    """ Prepares data for and calls clustering. Returns labels and scoring."""
    try:
        data = pd.read_csv(filename)
        data = data.loc[:, columns]
        data = preprocessing.scale(data)
        kmeans = sf_kmeans.SF_KMeans(n_clusters=k, n_init=n_init, covar_type='full', covar_tied=False)
        kmeans.fit(data)
        bic = kmeans.bic(data)
        labels = [int(l) for l in kmeans.labels_]
        return bic, labels
    except Exception as e:
        print("Error: " + e)
        return float("-inf"), []


def cluster_crops(filename, folder, crops, n_init=1, filter_members=10, columns=('latitude', 'longitude'),
                  k_range=range(2, 20), region='fresno', ext='.csv', result_folder='test'):
    print(folder + filename)
    for crop in crops:
        print('clustering {} started at {}.'.format(crop, datetime.now()))
        bestbic = float('-inf')
        bestcombo = []
        filename = crop + '_' + region + ext
        data = pd.read_csv(folder + filename)
        for k in k_range:
            for i in range(0, 10000):
                if len(data) < filter_members * k:
                    print('not enough data crop: {} k: {}'.format(crop, k))
                    break
                data_k = data
                bic, labels = run_kmeans(k, n_init, folder + filename, columns)
                members_per_cluster = np.bincount(labels, minlength=k)
                print('{}, {}, {}, {}'.format(crop, str(k), str(bic), str(members_per_cluster)))
                if len(labels) == 0 or np.min(members_per_cluster) < filter_members:
                    continue
                combo = [k, columns, labels]
                data_k['labels'] = labels
                data_k.to_csv('./{}/{}/kmeans_{}_{:02d}_{}_{}.csv'.format(result_folder, region, crop, k, i, bic))
                if bic > bestbic:
                    bestbic = bic
                    bestcombo = combo
        if len(bestcombo) == 0:
            print('no optimal solution {} min_memabers {}'.format(crop, filter_members))
        else:
            data['labels'] = bestcombo[2]
            data.to_csv("./{}/{}/best_kmeans_mah_{}_{:02d}.csv".format(result_folder, region, crop, bestcombo[0]))


#######################################
# Below is the history of experiments #
#######################################

# 10K experiment
def cluster_10000(filename, folder, crops, n_init=1, filter_members=20, columns=('latitude', 'longitude'),
                  k_range=range(1, 20), region='fresno', ext='.csv', result_folder='test'):
    print(folder + filename)
    for crop in crops:
        print('clustering {} started at {}.'.format(crop, datetime.now()))
        bestbic = float('-inf')
        bestcombo = []
        filename = crop + '_' + region + ext
        data = pd.read_csv(folder + filename)

        for k in k_range:
            print('clustering {} started at {}.'.format(crop, datetime.now()))
            stats = pd.DataFrame(columns=['result_folder', 'region', 'crop', 'k', 'i', 'bic', 'members_per_cluster'])
            for i in range(0, 1000):
                if len(data) < filter_members * k:
                    print('not enough data crop: {} k: {}'.format(crop, k))
                    break
                data_k = data.copy(deep=True)
                bic, labels = run_kmeans(k, n_init, folder + filename, columns)
                members_per_cluster = np.bincount(labels, minlength=k)
                # Uncomment below for filtering at runtime:
                # print('{}, {}, {}, {}'.format(crop, str(k), str(bic), str(members_per_cluster)))
                # if len(labels) == 0 or np.min(members_per_cluster) < filter_members:
                #     continue
                combo = [k, columns, labels]
                data_k['labels'] = labels
                data_k.to_csv('./{}/{}/kmeans_{}_{:02d}_{}_{}.csv'.format(result_folder, region, crop, k, i, bic))
                stats = stats.append({'result_folder': result_folder, 'region': region,
                                      'crop': crop, 'k': k, 'i': i, 'bic': bic,
                                      'members_per_cluster': members_per_cluster},
                                     ignore_index=True)
                if bic > bestbic:
                    bestbic = bic
                    bestcombo = combo
            stats.to_csv(crop + "_" + str(k) + '_stats.csv')
        if len(bestcombo) == 0:
            print('no optimal solution {} min_memabers {}'.format(crop, filter_members))
        else:
            data['labels'] = bestcombo[2]
            data.to_csv("./{}/{}/best_kmeans_mah_{}_{:02d}.csv".format(result_folder, region, crop, bestcombo[0]))
        print('clustering {} finished at {}.'.format(crop, datetime.now()))

########################
# Previous experiments #
########################


# def cluster():
#     n_init = 10
#     filter_members = 5
#     folder = '../../clustering/resources/'
#     crops = ['almonds', 'grapes', 'tomatoes', 'pistachios', 'citrus', 'idle']
#     cluster_crops(folder, crops, n_init, filter_members, result_folder='first_pass')


# def get_five_cluster():
#     n_init = 100
#     folder = '../../clustering/resources/crop_per_county/almonds/'
#     crops = ['almonds']
#     filenames = ['almonds_fresno.csv']  # 'idle_fresno.csv'
#     for filename in filenames:
#         cluster_crops(filename, folder, crops, n_init, filter_members=0,
#                       columns=('latitude', 'longitude'), k_range=range(2, 7), result_folder='five_clusters')
#

# def get_2_10_cluster_per_region_min_20():
#     n_init = 100
#     filter_members = 20
#     folder = '../../clustering/resources/crop_per_county/'
#     crops = ['almonds', 'grapes', 'tomatoes', 'pistachios', 'citrus', 'idle']
#     regions = ['fresno', 'kern']
#     for region in regions:
#         cluster_crops("", folder, crops, n_init, filter_members=filter_members,
#                       columns=('latitude', 'longitude'), k_range=range(2, 11), region=region, ext='csv',
#                       result_folder='per_region_k_2_10_min_mem_20')


# def get_wtd_2_10_cluster_per_region_min_20():
#     n_init = 100
#     filter_members = 20
#     folder = '../../clustering/resources/crop_per_county/wtd/'
#     crops = ['almonds', 'grapes', 'tomatoes', 'pistachios', 'citrus', 'idle']
#     regions = ['fresno', 'kern']
#     for region in regions:
#         cluster_crops("", folder, crops, n_init, filter_members=filter_members,
#                       columns=('latitude', 'longitude', '_mean'), k_range=range(2, 11), region=region, ext='_wt.csv',
#                       result_folder='wrd_per_region_k_2_10_min_mem_20')


# def get_wtdll_2_10_cluster_per_region_min_10():
#     n_init = 1
#     filter_members = 10
#     folder = '../../clustering/resources/crop_per_county/wtd/'
#     # crops = ['almonds', 'grapes', 'tomatoes', 'pistachios', 'citrus', 'idle']
#     crops = ['almonds']
#     regions = ['fresno', 'kern']
#     regions = ['kern']
#     columns = ('latitude', 'longitude', '_mean')
#     cluster_crops("", folder, crops, n_init, filter_members=filter_members,
#                   columns=columns, k_range=range(3, 4), region='kern',
#                   ext='_wt.csv', result_folder='follow_up_almond')
#     # for region in regions:
#     #     cluster_crops("", folder, crops, n_init, filter_members=filter_members,
#     #                   columns=columns, k_range=range(2, 11), region=region,
#     #                   ext='_wt.csv', result_folder='get_wtdll_2_10_cluster_per_region_min_10')
#     #
#     #


# def experiment_with_10000_runs():
#     # delano citrus and grapes
#     n_init = 1
#     filter_members = 20
#     folder = '../../clustering/resources/crop_per_county/wtd/'
#     crops = ['almonds', 'grapes', 'tomatoes', 'pistachios', 'citrus', 'idle']
#     regions = ['fresno', 'kern']
#     columns = ('latitude', 'longitude', '_mean')
#     for region in regions:
#         cluster_10000("", folder, crops, n_init, filter_members=filter_members,
#                   columns=columns, k_range=range(1, 11), region=region,
#                   ext='_wt.csv', result_folder='10000')


def experiment_with_10000_runs_grapes():
    n_init = 1
    filter_members = 20
    folder = '../../clustering/resources/crop_per_county/wtd/'
    crops = ['almonds', 'grapes', 'tomatoes', 'pistachios', 'citrus', 'idle']
    regions = ['fresno', 'kern']
    columns = ('latitude', 'longitude', '_mean')
    for region in regions:
        cluster_10000("", folder, crops, n_init, filter_members=filter_members,
                      columns=columns, k_range=range(1, 11), region=region,
                      ext='_wt.csv', result_folder='10000')


def main():
    # get_2_10_cluster_per_region_min_20()
    # get_wtd_2_10_cluster_per_region_min_20()
    # get_wtdll_2_10_cluster_per_region_min_10()
    experiment_with_10000_runs_grapes()


main()
