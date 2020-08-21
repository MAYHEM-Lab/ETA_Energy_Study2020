# Postprocessing of clustering files (used for 10K analysis).
import ast
import numpy as np


def filter_clusters(filename, min_members=20):
    # Given the cardinality of clusters, select the first non-degenerate one.
    with open(filename) as file:
        for line in file:
            line = line.strip()
            line = ast.literal_eval(line)
            line = np.array(line).astype(np.int)
            try:
                if np.min(line) > min_members:
                    print(line)
                    break
            except Exception as e:
                print(e)


def filter_results():
    folder = 'path-to-results-folder'
    crops = ['almonds', 'grapes', 'tomatoes', 'pistachios', 'citrus', 'idle']
    filenames = [folder + crop + '_stats/all_stats.csv' for crop in crops]
    for filename in filenames:
        filter_clusters(filename)
