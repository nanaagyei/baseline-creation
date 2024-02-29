from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import folium
from geopy import distance
import geopy.distance
from sklearn.neighbors import NearestNeighbors



#%%
# all functions:

def tuple_to_list(arr):
    my_list = [list(t) for t in arr]
    new_arr =  np.array(my_list)
    return new_arr

# slicing the df into a dataframe for each cluster
def single_hub_df(main_df, sub_df):
    mask = main_df["Lat dec"].isin(sub_df["Lat dec"]) & main_df["Long dec"].isin(sub_df["Long dec"])
    df_region = main_df[mask]
    return df_region

#function to compute distances
def comp_distances(df, column_name, index="Site Code"):
    df = df.reset_index(drop=True)
    true_df = df[df[column_name] == True].reset_index(drop=True)
    false_df=df[df[column_name] == False].reset_index(drop=True)
    dist = []
    true_dist = pd.DataFrame()
    for i in range(len(true_df[index])):
        for j in range(len(false_df[index])):
            trues = (true_df["Lat dec"][i], true_df["Long dec"][i])
            falses = (false_df["Lat dec"][j], false_df["Long dec"][j])
            dist.append(distance.distance(trues, falses, ellipsoid="GRS-80").km)
        true_dist[true_df[index][i]] = dist
        dist = []
    return true_dist.set_index(false_df[index])

#Sort the means
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
    false_df= df[df[column_name] == True].reset_index(drop=True)
    dist = []
    true_dist = pd.DataFrame()
    for i in range(len(true_df[index])):
        for j in range(len(false_df[index])):
            trues = (true_df["Lat dec"][i], true_df["Long dec"][i])
            falses = (false_df["Lat dec"][j], false_df["Long dec"][j])
            dist.append(distance.distance(trues, falses, ellipsoid="GRS-80").km)
        true_dist[true_df[index][i]] = dist
        dist = []
    return true_dist.set_index(false_df[index])

#%%
# Define a function to calculate the distance between two points
def calc_distance(point1, point2):
    return geopy.distance.distance(point1, point2,ellipsoid="GRS-80").km

#%%
# Read excel file
file_path = r"D:\baseline creation\NETWORK COORDINATES.xlsx"

# Assign excel file to panda dataframe
df = pd.read_excel(file_path)

#%%
## HUB SELECTION 

#Output the summary of the distances
dist_summary = comp_distances(df,"NGS CORS","Site Code")
# print(dist_summary)

#Output the sorted average of the distances in ascending order(smallest to largest)
means = get_sorted_means(dist_summary)
# print("_"*70 + "Average distances" + "_"*70)
# print(means)   

#Extract the least of the averaged distance into a variable called selected_single_hub
all_hubs = list(means.keys())
# print("Suggested Hubs are:",all_hubs)



#%%
#compute distances from stations to CORS and extract each of their least distance to a cors

# Select only the rows where NGS CORS is False
df_cors_false = df[df["NGS CORS"] == False]

# Compute the distances between the points with NGS CORS=False and the points with NGS CORS=True
distances = comp_distances(df, "NGS CORS")

# Find the index of the minimum distance for each point with NGS CORS=False
min_distance_index = distances.idxmin(axis=1)

# Create a new dataframe to store the minimum distances
df_min_distances = pd.DataFrame(columns=["start", "end", "min_distance"])

# Iterate over the index of the minimum distances
for index, min_distance in min_distance_index.items():
    # Get the start and end points and the minimum distance
    start = index
    end = min_distance
    distance = distances.loc[index, min_distance]
    # Add the start, end, and minimum distance to the dataframe
    df_min_distances = pd.concat([df_min_distances, pd.DataFrame({"start": [start], "end": [end], "min_distance": [distance]})], ignore_index=True)

# Display the resulting dataframe
# print(df_min_distances)



#%%
##Compute the distnaces between the CORS and find the shortest distances 


# Define the dataframe to use
true_df = df[df["NGS CORS"] == True]

# Get the number of rows in the dataframe
n = df.shape[0] - df_min_distances.shape[0] - 1
print(n)

# Initialize an empty list to store the distances
distances = []

# Iterate over the rows of the true_df DataFrame
for i, row in true_df.iterrows():
    # Calculate the distance to all other points
    for j, other_row in true_df.iterrows():
        if i != j:
            point1 = (row["Lat dec"], row["Long dec"])
            point2 = (other_row["Lat dec"], other_row["Long dec"])
            distance = calc_distance(point1, point2)
            distances.append((distance, row["Site Code"], other_row["Site Code"]))

# Sort the list of distances in ascending order
distances.sort()

selected_distances = {}
selected_points = set()
count = 0

for distance, start, end in distances:
    if (start != end) and (start not in selected_points) and (end not in selected_points) and count < n*2:
        selected_distances[f"{start} to {end}"] = distance
        count += 1
        selected_points.add(start)
        selected_points.add(end)
    if count == n * 2:
        break

# Print the selected distances
print(selected_distances)


# # Define the dataframe to use
# true_df = df[df["NGS CORS"] == True]

# # Get the number of rows in the dataframe
# n = df.shape[0] - df_min_distances.shape[0] - 1
# # print(n)

# # Initialize an empty DataFrame to store the distances
# distances_df = pd.DataFrame(columns=["start", "end", "distance"])

# # Iterate over the rows of the DataFrame
# for i, row in true_df.iterrows():
#     # Calculate the distance to all other points
#     for j, other_row in true_df.iterrows():
#         if i != j:
#             point1 = (row["Lat dec"], row["Long dec"])
#             point2 = (other_row["Lat dec"], other_row["Long dec"])
#             distance = calc_distance(point1, point2)
#             # Append the distance to the DataFrame
#             temp_df = pd.DataFrame({"start": [row["Site Code"]], "end": [other_row["Site Code"]], "distance": [distance]})
#             distances_df = pd.concat([distances_df, temp_df], ignore_index=True)

# # Sort the DataFrame by the distance column in ascending order
# distances_df.sort_values("distance", inplace=True)



# selected_distances_df = pd.DataFrame(columns=["start", "end", "distance"])

# # Initialize variables to store the previous start and end points
# previous_start = None
# previous_end = None

# # Initialize a count variable to keep track of the number of selected distances
# count = 0

# # # Initialize a set to store the selected "start" and "end" values
# # selected_points = set()

# # # Iterate over the rows of the sorted DataFrame
# # for i, row in distances_df.iterrows():
# #     # Check if either the "start" or "end" value is already in the set
# #     if row["start"] in selected_points:
# #         new_start = row["end"]
# #     elif row["end"] in selected_points:
# #         new_start = row["start"]
# #     else:
# #         new_start = row["start"]
# #     # Append the new "start" value to the set
# #     selected_points.add(new_start)
# #     # Append the new "start" and "end" values to the selected_distances_df
# #     selected_distances_df = pd.concat([selected_distances_df, pd.DataFrame({"start": [new_start], "end": [row["end"]], "distance": [row["distance"]]})], ignore_index=True)
# #     # Check if the number of selected distances is equal to n
# #     if len(selected_points) == n:
# #         break


# # Iterate over the rows of the sorted DataFrame
# for i, row in distances_df.iterrows():
#     # Check if the start and end points are unique


#     if (row["start"] != row["end"]) and \
#        (row["start"] != previous_start or row["end"] != previous_end) and \
#        (row["start"] != previous_end or row["end"] != previous_start) and \
#        (row["start"] not in selected_distances_df["start"].tolist() or row["end"] not in selected_distances_df["end"].tolist()):

#     # if (row["start"] != row["end"]) and \
#     #    (row["start"] not in selected_distances_df["start"].tolist() and row["end"] not in selected_distances_df["end"].tolist()):

#     # if (row["start"] != row["end"]) and \
#     #    (row["start"] != previous_start or row["end"] != previous_end) and \
#     #    (row["start"] != previous_end or row["end"] != previous_start):
#         # Append the row to the selected_distances_df
#         selected_distances_df = pd.concat([selected_distances_df, row.to_frame().T], axis=0)
        
        
#         # Update the previous start and end points
#         previous_start = row["start"]
#         previous_end = row["end"]
        
#         # Increment the count
#         count += 1
        
#         # Check if the count is equal to n
#         if count == n:
#             break


# # Print the selected distances DataFrame
# print(selected_distances_df)

# Define the dataframe to use
# true_df = df[df["NGS CORS"] == True]

# # Get the number of rows in the dataframe
# n = df.shape[0] - df_min_distances.shape[0] - 1
# # print(n)

# # Initialize an empty DataFrame to store the distances
# distances_df = pd.DataFrame(columns=["start", "end", "distance"])

# # Iterate over the rows of the DataFrame
# for i, row in true_df.iterrows():
#     # Calculate the distance to all other points
#     for j, other_row in true_df.iterrows():
#         if i != j:
#             point1 = (row["Lat dec"], row["Long dec"])
#             point2 = (other_row["Lat dec"], other_row["Long dec"])
#             distance = calc_distance(point1, point2)
#             # Append the distance to the DataFrame
#             temp_df = pd.DataFrame({"start": [row["Site Code"]], "end": [other_row["Site Code"]], "distance": [distance]})
#             distances_df = pd.concat([distances_df, temp_df], ignore_index=True)

# # Sort the DataFrame by the distance column in ascending order
# distances_df.sort_values("distance", inplace=True)

# selected_distance_df = pd.DataFrame(columns=["start", "end", "distance"])
# count = 0

# for i, row in distances_df.iterrows():
#     if count >= n:
#         break
#     if (row["start"] not in selected_distance_df["start"]) and (row["start"] not in selected_distance_df["end"]) and (row["end"] not in selected_distance_df["start"]) and (row["end"] not in selected_distance_df["end"]) and ((row["start"], row["end"]) not in set(zip(selected_distance_df["end"], selected_distance_df["start"]))) and ((row["start"] not in selected_distance_df["start"]) or (row["end"] not in selected_distance_df["end"])):
#         selected_distance_df = selected_distance_df.append(row)
#         count += 1



# print(selected_distance_df)



# # """
# # For each row, it will check if either the "start" or "end" value is already in the set. If it is, 
# # then select the other point (the one that is not in the set) as the new "start" or "end" value.
# # """

# # %%
# # POPULATE OPUS PROJECT JOB INPUT FILE xml file
# import xml.etree.ElementTree as ET
# from xml.dom import minidom

# # create root element
# root = ET.Element('OPTIONS')

# # create BASELINES element
# baselines = ET.SubElement(root, 'BASELINES')

# # Iterate over the rows of the hub_baselines_df DataFrame
# for i, row in df_min_distances.iterrows():
#     # Extract the start and end point codes
#     start = row["start"]
#     end = row["end"]
    
#     # Create a DISTANCE element
#     distance = ET.SubElement(baselines, 'DISTANCE')
#     # Create a FROM element and set its text to the value of the start point code
#     from_point = ET.SubElement(distance, 'FROM')
#     from_point.text = start
#     # Create a TO element and set its text to the value of the end point code
#     to_point = ET.SubElement(distance, 'TO')
#     to_point.text = end


# for i, row in selected_distances_df.iterrows():
#     # Extract the start and end point codes
#     start = row["start"]
#     end = row["end"]
    
#     # Create a DISTANCE element
#     distance = ET.SubElement(baselines, 'DISTANCE')
#     # Create a FROM element and set its text to the value of the start point code
#     from_point = ET.SubElement(distance, 'FROM')
#     from_point.text = start
#     # Create a TO element and set its text to the value of the end point code
#     to_point = ET.SubElement(distance, 'TO')
#     to_point.text = end

# all_hubs_df = df[df["NGS CORS"] == True]
# all_hubs_sitecode = all_hubs_df.loc[:, "Site Code"]
# all_hubs_sitecode_df = all_hubs_sitecode.to_frame()

# # print (all_hubs_sitecode_df)

# # create CORS element 
# # Shows cors that must be included
# cors = ET.SubElement(root, 'CORS')
# for i, row in all_hubs_sitecode_df.iterrows():
#     hub1 = ET.SubElement(cors, 'HUB')
#     hub1.text = row["Site Code"]
#     fix1 = ET.SubElement(hub1, 'FIX')
#     fix1.text = '3-D'


# # # prettify the XML and print it
# # xml_str = minidom.parseString(ET.tostring(root)).toprettyxml()
# # print(xml_str)

# ##find all the DISTANCE elements in the BASELINES element
# distances = baselines.findall('DISTANCE')
# # print the number of DISTANCE elements
# print(len(distances))



# #%% 
# #map display

# import folium
# from folium.vector_layers import Circle, PolyLine
# import pandas as pd
# from PySide6.QtWebEngineWidgets import QWebEngineView
# from PySide6.QtWidgets import QApplication
# from folium.features import Tooltip, Popup
# from IPython.display import display

# #splitting start and end into separate dataframes, so that i can mask them in the main df to obtain coordinates
# all_hubs_start_df = df_min_distances[['start']]
# all_hubs_start_final_df = pd.DataFrame(columns=df.columns)
# for value in all_hubs_start_df['start']:
#     temp_start_df = df.loc[df['Site Code'] == value]
#     all_hubs_start_final_df = pd.concat([all_hubs_start_final_df,temp_start_df], ignore_index=True)



# all_hubs_end_df = df_min_distances[['end']]
# all_hubs_end_final_df = pd.DataFrame(columns=df.columns)
# for value in all_hubs_end_df['end']:
#     temp_end_df = df.loc[df['Site Code'] == value]
#     all_hubs_end_final_df = pd.concat([all_hubs_end_final_df,temp_end_df], ignore_index=True)

# # print(df_min_distances)
# # print(all_hubs_start_final_df)
# # print(all_hubs_end_final_df)







# #splitting done for the hub connection too

# hubs_connection_start_df = selected_distances_df[['start']]
# hubs_connection_start_final_df = pd.DataFrame(columns=df.columns)
# for value in hubs_connection_start_df['start']:
#     temp_hub_connection_start_df = df.loc[df['Site Code'] == value]
#     hubs_connection_start_final_df  = pd.concat([hubs_connection_start_final_df ,temp_hub_connection_start_df], ignore_index=True)


# hubs_connection_end_df = selected_distances_df[['end']]
# hubs_connection_end_final_df = pd.DataFrame(columns=df.columns)
# for value in hubs_connection_end_df['end']:
#     temp_hub_connection_end_df = df.loc[df['Site Code'] == value]
#     hubs_connection_end_final_df  = pd.concat([hubs_connection_end_final_df ,temp_hub_connection_end_df], ignore_index=True)

# print(selected_distances_df)
# print(hubs_connection_start_final_df)
# print(hubs_connection_end_final_df)





# # Select all rows with True in the NGS CORS column
# df_hubs = df.loc[df['NGS CORS'] == True]

# # Select all rows with False in the NGS CORS column
# df_other = df.loc[df['NGS CORS'] == False]

# #%%
# # Create a map centered on the mean of the locations in the dataframe
# mean_lat = df['Lat dec'].mean()
# mean_lon = df['Long dec'].mean()
# map = folium.Map(location=[mean_lat, - mean_lon], zoom_start=6.5)


# # Create a FeatureGroup for the polylines
# polyline_layer = folium.FeatureGroup(name='Baselines')

# # Create a FeatureGroup for the first markers
# ngs_cors_marker_layer = folium.FeatureGroup(name='NGS CORS')

# # Create a FeatureGroup for the second markers
# stations_marker_layer = folium.FeatureGroup(name='Stations')

# # Add the FeatureGroups to the map
# polyline_layer.add_to(map)
# ngs_cors_marker_layer.add_to(map)
# stations_marker_layer.add_to(map)


# # Add a marker for each location in the dataframe
# for index, row in df_hubs.iterrows():
#     lat = row['Lat dec']
#     lon = row['Long dec']
#     site_code = row['Site Code']
    

#     # Create the label content
#     label = Tooltip(site_code)
#     popup = Popup(site_code)  # Create the pop-up content

#     #create marker
#     marker = Circle(location=[lat, -lon], radius=5000, color='red', fill_color='red',fill_opacity =1, tooltip=label,popup = popup)
#     marker.add_to(ngs_cors_marker_layer)
#     ngs_cors_marker_layer.add_to(map)



# for index, row in df_other.iterrows():
#     lat = row['Lat dec']
#     lon = row['Long dec']
#     site_code = row['Site Code']
    

#     # Create the label content
#     label = Tooltip(site_code)
#     popup = Popup(site_code)  # Create the pop-up content

#     #create marker
#     marker= Circle(location=[lat, -lon], radius=5000, color='blue', fill_color='blue',fill_opacity =1, tooltip=label,popup = popup)
#     marker.add_to(stations_marker_layer)
#     stations_marker_layer.add_to(map)






# # Iterate over the rows of connections to generate baselines between stations and hubs
# for i, row in all_hubs_start_final_df.iterrows():
#     # Get the coordinates of the start marker
#     start_coords = [row['Lat dec'], -row['Long dec']]
#     # Get the coordinates of the end marker
#     end_coords = [all_hubs_end_final_df.loc[i, 'Lat dec'], -all_hubs_end_final_df.loc[i, 'Long dec']]
#     # Create the PolyLine object
#     line = folium.PolyLine(locations=[start_coords, end_coords], color='blue', weight=2, opacity=1)
#     # Add the line to the polyline layer
#     polyline_layer.add_child(line)
#     # Add the polyline layer to the map
#     polyline_layer.add_to(map)



# # Iterate over the rows of connections to generate baselines between hubs
# for i, row in  hubs_connection_start_final_df.iterrows():
#     # Get the coordinates of the start marker
#     start_coords = [row['Lat dec'], -row['Long dec']]
#     # Get the coordinates of the end marker
#     end_coords = [hubs_connection_end_final_df.loc[i, 'Lat dec'], -hubs_connection_end_final_df.loc[i, 'Long dec']]
#     # Create the PolyLine object
#     line = folium.PolyLine(locations=[start_coords, end_coords], color='blue', weight=2, opacity=1)
#     # Add the line to the polyline layer
#     polyline_layer.add_child(line)
#     # Add the polyline layer to the map
#     polyline_layer.add_to(map)




# # Create a Stamen Toner tileset
# stamen_toner = folium.TileLayer(
#     tiles='https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
#     attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.',
#     name='Stamen Toner',
#     max_zoom=18,
#     min_zoom=0,
#     show=True
# )

# # Add the tileset to the map
# stamen_toner.add_to(map)

# # Add the layer control to the map
# folium.LayerControl().add_to(map)

# # Add the Stamen Toner tileset to the map
# stamen_toner.add_to(map)

# # Save the map to an HTML file
# map.save('map.html')


# # Create the PySide6 application
# app = QApplication()

# # Create the QWebView widget and set its size
# view = QWebEngineView()
# # view.resize(400, 300)

# # Load the map into the widget
# view.setHtml(map._repr_html_())

# # Show the widget
# view.show()

# # Run the PySide6 application
# app.exec()
