import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.metrics import davies_bouldin_score
from sklearn import decomposition
import random
import matplotlib.pyplot as plt
random.seed(11)

def create_data_frame(directory,save_to_csv):
    """ 
    Creates a data frame consisting of all the .csv-files in a given directory. The directory should
    be where the unzipped data files are stored. Assumes the data file benign_traffic.csv has not had a 
    name change.
    
    Parameters
    ----------
    directory : str
        The directory in which the data files are stored. 
    save_to_file : boolean
        Boolean for determining if the data frame should be saved to a .csv-file in the directory    
        
    Returns
    -------
    data : pandas data frame 
        consisting of all the original data files combined into one. The rows are instances of
        traffic and the columns are the same as described by Meidan et al.
    """
    files_in_directory = os.listdir('{directory}/'.format(directory = directory))
    csv_files = list(filter(lambda x: 'csv' in x, files_in_directory)) # need to exclude the benign ones
    csv_files = list(filter(lambda x: 'benign' not in x, csv_files))
    data = pd.read_csv('{directory}benign_traffic.csv'.format(directory=directory))
    data['label'] = 'benign_traffic'
    
    for file_name in csv_files:
        data_frame = pd.read_csv(directory + file_name)
        data_frame['label'] = file_name.split('.')[0]
        data = data.append(data_frame)
    
    if save_to_csv:
        device_name = directory.split('/')[-2]
        data.to_csv(directory + '/' + device_name + '.csv')
        
    return(data)

def create_distribution_data_frames(k,data):
    """
    Creates a dictionary of data frames, one for each cluster in the chosen clustering solution,
    where each data frame contains information about the make-up of traffic in that cluster. The columns
    are "traffic_type" (string) and "percentage" (float), where each row gives the percentage of points
    in a cluster belonging to a given traffic_type. E.g. a row with values "scan_gafgyt" and 0.5 means
    50% of all the points in that cluster have the label "scan_gafgyt".
    
    Parameters
    ----------
    k : int
        Number of cluster from a clustering solution.
    data : pandas dataframe
        Data frame created by create_data_frame with an added column "cluster_assignment",
        this column should be the labels assigned from a clustering algorithm.
        
    Returns
    -------
    dict_of_dataframes : dict
        Dictionary of dataframes. The keys are the cluster indices from the clustering algorithm.
    
    """
    
    k_values = list(range(0,k))
    dict_list = [-1]*k
    counts_list = [-1]*k
    for k_val in k_values:
        cluster = data.loc[data['cluster_assignment'] == k_val,'label']
        unique, counts = np.unique(cluster, return_counts=True)
        n_rows = cluster.shape[0]
        
        counts_dict = {'cluster number' : k_val, 'nr_of_obs_in_cluster' : n_rows}
        
        proportions = counts/n_rows
        proportions = proportions.round(4)
        df_dict = {'proportions' : proportions, 'traffic_type' : unique}
        pd_data_frame = pd.DataFrame(df_dict)
        
        dict_list[k_val] = pd_data_frame
        counts_list[k_val] = counts_dict
        
    dict_of_dataframes = dict(zip(k_values,dict_list))
    dict_of_counts = dict(zip(k_values,counts_list))   
    return_dict = {'dict_of_dataframes' : dict_of_dataframes, 'dict_of_counts' : dict_of_counts}
    return(return_dict)

def select_n_components(explained_variance_list,percentage_chosen):
    """
    Gives the number of principal components required to explain 90% of the variation
    based on a list of pca explained variance ratios.  Note : Requires a sklearn.decomposition.PCA-
    object to be created first.
    
    Parameters
    ----------
    explained_variance_list : numpy.ndarray
        Result of sklearn.decomposition.PCA.explained_variance_ratio_, contains the proportion
        of variance explained by each principal component.
    
    percentage_chosen : float
        Percentage of the variation in the data which must be explained by the principal components. 
        
    Returns
    -------
    i : int
        The number of principal components required to explain at least percentage_chosen% of the data.
    """    
    cumulative_sum = np.cumsum(explained_variance_list)
    
    total_nr_components = len(explained_variance_list)
    for i in range(total_nr_components):
        if cumulative_sum[i] > percentage_chosen:
            return(i+1)
  
def calculate_db_scores(k_range,data):
    """
    Calculates the Davies-Bouldin indices for different values of K in K-means clustering.
    
    Parameters
    ----------
    k_range : list
        list of ints which are the different values of K to be used as input in K-means
    data : numpy.ndarray
        numpy.ndarray which contains the data points to be clustered.

    Returns
    -------
    db_values : dict
        Dictionary where the number of clusters in a solution are the keys and the corresponding
        Davies-Bouldin indices are the values.

    """
    
    db_vector = []
    for k in k_range:
        kmeans_result = KMeans(n_clusters=k,init='random',random_state=11).fit(data)
        db_vector.append(davies_bouldin_score(data,kmeans_result.labels_))
    db_values = dict(zip(k_range,db_vector))    
    return(db_values)

def plot_and_save_proportions(dataframe_dictionary,directory):
    """
    Creates matplotlib plots showing the distribution of traffic types in the
    different clusters.

    Parameters
    ----------
    dataframe_dictionary : dict
        Object created by create_distribution_data_frames(). The keys are the cluster indices
        while the values contain the proportions showing the make-up of traffic in each cluster.
    directory : str
        Directory where the figures should be saved.

    Returns
    -------
    None.

    """
    
    clusters = list(dataframe_dictionary.keys())
    nr_of_clusters = len(clusters)
    
    for  k in range(nr_of_clusters):
        cluster = dataframe_dictionary.get(k)
        cluster.plot(kind='scatter',x='proportions',y='traffic_type',color='red')
        plt.savefig(directory+'cluster_{k}.png'.format(k = k),bbox_inches='tight')

def distribution_of_points(data_frame):
    # for each value of "label", find out how the points were distributed across the clusters
    labels = np.unique(data_frame['label'])
    nr_of_labels = labels.shape[0]
    proportions_list = [-1]*nr_of_labels
    return_string_list = [-1]*nr_of_labels

    for i in range(nr_of_labels):
        data_points = data_frame.loc[data_frame['label'] == labels[i],'cluster_assignment']
        clusters, amount_of_obs_with_label_in_cluster = np.unique(data_points, return_counts=True)
        return_string = labels[i] +' '
        cluster_dict = {'clusters':clusters,'nr_of_obs_with_label' : amount_of_obs_with_label_in_cluster}
        return_string_list[i] = return_string + str(cluster_dict)
    return(return_string_list)    
        
def run_analysis(device_directory,proprtion_of_variance_to_explain,save_to_csv,save_pca_to_csv):
    device_data = create_data_frame(device_directory,save_to_csv)
    data_matrix = device_data.drop(labels=["label"],axis=1)
    scaler = preprocessing.StandardScaler() 
    data_matrix = scaler.fit_transform(data_matrix)
    
    # PCA
    pca = decomposition.PCA()
    pca_fit = pca.fit(data_matrix)
    cumulative_sum = np.cumsum(pca_fit.explained_variance_ratio_)
    nr_of_components = select_n_components(pca_fit.explained_variance_ratio_,proprtion_of_variance_to_explain)

    pca = decomposition.PCA(n_components = nr_of_components)
    pca_fit = pca.fit(data_matrix)
    data_matrix = pca_fit.fit_transform(data_matrix)
    
    # save the PCA results as well
    if save_pca_to_csv:
        print('saving PCA csv')
        file_name = device_directory.split('/')[-2]
        directory = '/'.join(device_directory.split('/')[:-2])
        data_frame = pd.DataFrame(data=data_matrix)
        print(directory + '/' + file_name + '/' + file_name + '_pca.csv') 
        data_frame.to_csv(directory + '/' + file_name + '/' + file_name + '_pca.csv')
    
    db_values = calculate_db_scores(list(range(2,12)),data_matrix)
    minimum_db = min(db_values.items(), key=lambda x: x[1]) 
    k = minimum_db[0]
    min_db = minimum_db[1]
    
    kmeans_result = KMeans(n_clusters=k,init='random',random_state=11).fit(data_matrix)
    device_data['cluster_assignment'] = kmeans_result.labels_
        
    dict_from_data = create_distribution_data_frames(k, device_data)
    dataframe_dict = dict_from_data['dict_of_dataframes']
    counts_dict = dict_from_data['dict_of_counts']
    
    plot_and_save_proportions(dataframe_dict,device_directory)
    
    distribution_string = 'Distribution of the labels among the different clusters: ' + '\n' + str(distribution_of_points(device_data))
    
    # save output to file, nr_of_components, k, db-values
    device_name_string = device_directory.split('/')[0] + '\n'
    principal_component_string = 'Number of principal components used to explain {percentage} of the variation : {nr_of_components}'.format(percentage = proprtion_of_variance_to_explain, nr_of_components = nr_of_components) + '\n'
    davies_bouldin_string = 'Davies-Bouldin indices : {db_values}'.format(db_values = db_values) + '\n'
    best_solution_string = 'The lowest value of the Davies-Bouldin index ({min_db}) was obtained for K = {k}'.format(min_db = min_db, k = k) + '\n'
    counts_string = 'Number of obs in the different clusters: ' + '\n' + str(counts_dict) + '\n'
    output_string = device_name_string + principal_component_string + davies_bouldin_string + best_solution_string + counts_string + distribution_string + '\n'
    
    output_file = open(device_directory +'output_file.txt',"w") 
    output_file.write(output_string) 
    output_file.close() 