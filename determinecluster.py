from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#%%%
# Read excel file
file_path = r"D:\baseline creation\NETWORK COORDINATES.xlsx"

# Assign excel file to panda dataframe
df = pd.read_excel(file_path)
print(df)

#ectract long and lat from xcel file
cluster_df = df[['Site Code','Lat dec','Long dec']]
lo_la_df = df[['Lat dec','Long dec']]
# print(cluster_df)

# print(len(cluster_df))
#convert into list
lo_la_list = lo_la_df.values.tolist()
# print(lo_la_list)


X = np.array(lo_la_list)


#%%
##elbow method
# Create a list of within-cluster sum of squares for different values of k
# wcss = []
# for k in range(1, 10):
#     kmeans = KMeans(n_clusters=2, n_init='auto')
#     kmeans.fit(X)
#     wcss.append(kmeans.inertia_)

# # Plot the within-cluster sum of squares for each value of k
# plt.plot(range(1, 10), wcss)
# plt.xlabel('Number of clusters')
# plt.ylabel('Within-cluster sum of squares')
# plt.show()


#%%
# Create a list of silhouette scores for different values of k
scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=2, n_init='auto')
    kmeans.fit(X)
    labels = kmeans.predict(X)
    score = silhouette_score(X, labels)
    scores.append(score)

# Plot the silhouette scores for each value of k
plt.plot(range(2, 11), scores)
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette score')
plt.show()


#%%

#Create a list of silhouette scores for different values of k
# scores = []
# for k in range(2, 11):
#     kmeans = KMeans(n_clusters=k,n_init='auto')
#     kmeans.fit(X)
#     labels = kmeans.predict(X)
#     score = silhouette_score(X, labels)
#     scores.append(score)

# # Find the value of k with the highest silhouette score
# best_k = np.argmax(scores) + 2

# # Plot the silhouette scores for each value of k
# plt.plot(range(2, 11), scores)
# plt.xlabel('Number of clusters')
# plt.ylabel('Silhouette score')

# # Annotate the plot with the optimal value of k
# plt.annotate(f'k = {best_k}', xy=(best_k, scores[best_k - 2]), xytext=(best_k + 1, scores[best_k - 2] + 0.1),
#              arrowprops=dict(facecolor='red', shrink=0.05))

# plt.show()


# Extract information from the plot
# xmin, xmax = plt.xlim()
# ymin, ymax = plt.ylim()
# xticks, xticklabels = plt.xticks()
# yticks, yticklabels = plt.yticks()

# # Print the output as text
# print(f'x-axis limits: {xmin} to {xmax}')
# print(f'y-axis limits: {ymin} to {ymax}')
# print(f'x-axis tick marks: {xticks}')
# print
