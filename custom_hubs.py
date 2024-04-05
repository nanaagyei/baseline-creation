from folium.features import Tooltip, Popup
from PySide6.QtWebEngineWidgets import QWebEngineView
from folium.vector_layers import Circle, PolyLine
from sklearn.cluster import KMeans
from xml.dom import minidom
import sqlite3
import numpy as np
import pandas as pd
import openpyxl
import folium
from geopy import distance
import geopy.distance
from sklearn.neighbors import NearestNeighbors
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostringlist
import fileloader
import sys
from PySide6.QtWidgets import QApplication
import pickle


# %%

# all functions:

def tuple_to_list(arr):
    my_list = [list(t) for t in arr]
    new_arr = np.array(my_list)
    return new_arr

# slicing the df into a dataframe for each cluster


def single_hub_df(main_df, sub_df):
    mask = main_df["Lat dec"].isin(
        sub_df["Lat dec"]) & main_df["Long dec"].isin(sub_df["Long dec"])
    df_region = main_df[mask]
    return df_region

# function to compute distances


def comp_distances(df, column_name, index="Site Code"):
    df = df.reset_index(drop=True)
    true_df = df[df[column_name] == True].reset_index(drop=True)
    false_df = df[df[column_name] == False].reset_index(drop=True)
    dist = []
    true_dist = pd.DataFrame()
    for i in range(len(true_df[index])):
        for j in range(len(false_df[index])):
            trues = (true_df["Lat dec"][i], true_df["Long dec"][i])
            falses = (false_df["Lat dec"][j], false_df["Long dec"][j])
            dist.append(distance.distance(
                trues, falses, ellipsoid="GRS-80").km)
        true_dist[true_df[index][i]] = dist
        dist = []
    return true_dist.set_index(false_df[index])

# Sort the means


def get_sorted_means(summary):
    means = dict(summary.mean())
    means = {k: v for k, v in sorted(means.items(), key=lambda item: item[1])}
    return means


def remove_selected_hub(site_code_dict, selected_single_hub):
    value_to_remove = selected_single_hub
    keys_to_remove = []

    for key, value in site_code_dict.items():
        if value == value_to_remove:
            keys_to_remove.append(key)

    for one_key in keys_to_remove:
        site_code_dict.pop(one_key)


def comp_cors_distances(df, column_name, index="Site Code"):
    df = df.reset_index(drop=True)
    true_df = df[df[column_name] == True].reset_index(drop=True)
    false_df = df[df[column_name] == True].reset_index(drop=True)
    dist = []
    true_dist = pd.DataFrame()
    for i in range(len(true_df[index])):
        for j in range(len(false_df[index])):
            trues = (true_df["Lat dec"][i], true_df["Long dec"][i])
            falses = (false_df["Lat dec"][j], false_df["Long dec"][j])
            dist.append(distance.distance(
                trues, falses, ellipsoid="GRS-80").km)
        true_dist[true_df[index][i]] = dist
        dist = []
    return true_dist.set_index(false_df[index])

# %%
# Define a function to calculate the distance between two points


def calc_distance(point1, point2):
    return geopy.distance.distance(point1, point2, ellipsoid="GRS-80").km


1

# %%
# Read excel file
# file_path = r"D:\baseline creation\NETWORK COORDINATES.xlsx"
file_path = r"D:\baseline creation\SC NETWORK COORDINATES.xlsx"

# Assign excel file to panda dataframe
df = pd.read_excel(file_path)
# print(df)

# ectract long and lat from xcel file
cluster_df = df[['Site Code', 'Lat dec', 'Long dec']]
lo_la_df = df[['Lat dec', 'Long dec']]
# print(cluster_df)

# print(len(cluster_df))
# convert into list
lo_la_list = lo_la_df.values.tolist()
# print(lo_la_list)83

# %%
# CUSTOM CLUSTERING
# Clustering
X = np.array(lo_la_list)
# Prompt user for number of clusters
num_clusters = input("Enter the number of clusters: ")

# Convert user input to integer
num_clusters = int(num_clusters)

# Generate empty lists to store clusters
clusters = []
for i in range(num_clusters):
    clusters.append([])

# Perform clustering and store clusters in lists
kmeans = KMeans(n_clusters=num_clusters, n_init='auto', random_state=0).fit(X)
labels = kmeans.predict(X)

for i in range(len(X)):
    clusters[labels[i]].append(X[i])

# Create dataframes for each cluster
df_clusters = []
selected_hubs = []
site_code_dicts = []


# FOR SINGLE HUB

# for i in range(num_clusters):
#     # Create dataframe for current cluster
#     cluster_df = pd.DataFrame(clusters[i], columns=['Lat dec', 'Long dec'])
#     cluster_df["Site Code"] = df["Site Code"]

#     # Compute distances and select hub site code for current cluster
#     single_df = single_hub_df(df, cluster_df)
#     df_clusters.append(single_df)
#     dist_summary = comp_distances(single_df,"NGS CORS","Site Code")
#     print("Distance Summary: ")
#     print(dist_summary)
#     print("="*70)
#     means = get_sorted_means(dist_summary)
#     print("Means: ")
#     print(means)
#     print("="*70)
#     selected_single_hub = list(means.keys())[0]
#     selected_hubs.append(selected_single_hub)

# print(selected_hubs)

# FOR CUSTOM HUB
# Prompt user for number of single hub sites to select
num_hubs = input("Enter the number of single hub sites to select: ")

# Convert user input to integer
num_hubs = int(num_hubs)

for i in range(num_clusters):
    # Create dataframe for current cluster
    cluster_df = pd.DataFrame(clusters[i], columns=['Lat dec', 'Long dec'])
    cluster_df["Site Code"] = df["Site Code"]

    # Compute distances and select hub site code for current cluster
    single_df = single_hub_df(df, cluster_df)
    df_clusters.append(single_df)
    dist_summary = comp_distances(single_df, "NGS CORS", "Site Code")
    # print("Distance Summary: ")
    # print(dist_summary)
    # print("="*70)
    # Select the top num_single_hubs sites according to mean distance
    means = get_sorted_means(dist_summary)
    print("Means: ")
    print(means)
    print("="*70)
    # If user input exceeds the number of sites in the cluster, print "yawa"
    if num_hubs > len(means):
        print("yawa")
    else:
        custom_hubs = list(means.keys())[:num_hubs]
        selected_hubs.extend(custom_hubs)

print(selected_hubs)

# for all hubs
# for i in range(num_clusters):
#     # Create dataframe for current cluster
#     cluster_df = pd.DataFrame(clusters[i], columns=['Lat dec', 'Long dec'])
#     cluster_df["Site Code"] = df["Site Code"]

#     # Compute distances and select hub site code for current cluster
#     single_df = single_hub_df(df, cluster_df)
#     df_clusters.append(single_df)
#     dist_summary = comp_distances(single_df,"NGS CORS","Site Code")
#     print("Distance Summary: ")
#     print(dist_summary)
#     print("="*70)
#     means = get_sorted_means(dist_summary)
#     print("Means: ")
#     print(means)
#     print("="*70)
#     all_hubs = list(means.keys())
#     selected_hubs.append(all_hubs)

# print(selected_hubs)

# Extract rows corresponding to selected hub site codes
# mask = df["Site Code"].isin(selected_hubs)
# new_df = df[mask]
# print(new_df)
