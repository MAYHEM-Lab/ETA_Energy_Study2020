
### ETa and Energy Study 2020

#### Scripts

Energy and ETa data come as a group of daily (csv) files.

- _parsing_input_files.py_ flattens this data into a single file (hundreds of MiB).

- _eta_data_analysis.py_ prepares ETa data for visualization.

- _power_data_analysis.py_ prepares power data for visualization.

The last two files have utilities for indexing, parsing time,
aggregating power usage or ETa values, selecting data based on crop type,
location, or power usage type.

- _visualization.py_ combines Pandas data frames produced
with the previous files and plots them.

#### Clustering
- Methods for GMM, K-means (_gmm_clustering.py_), and extended K-means with Mahalanobis distance clustering (_mahalanobis_kmeans.py_).
- Methods for parsing (_filter_clusters.py_) and visualizing (_cluster_map_viz.py_) the results.
