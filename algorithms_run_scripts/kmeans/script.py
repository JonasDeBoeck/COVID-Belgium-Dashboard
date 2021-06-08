import pandas as pd
import numpy as np
from algorithms.kmeans.kmeans import *

representatives = ["WestVlaanderen", "Hainaut", "Brussels", "BrabantWallon"]

representatives_info = pd.read_csv("data\\filtered_data\KMEANS.csv")

representatives_info = representatives_info[representatives_info["PROVINCE"].isin(representatives)]
representatives_info = representatives_info[["INFECTION_RATE", "HOSPITALISATION_RATE", "TEST_POS_PERCENTAGE"]].to_numpy()

kmeans = Kmeans("data\filtered_data\KMEANS.csv", 4, representatives_info)
kmeans.start_clustering()