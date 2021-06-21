import pandas as pd
import numpy as np
from kmeans import Kmeans

representatives = ["WestVlaanderen", "Hainaut", "Brussels", "BrabantWallon"]

representatives_info = pd.read_csv("/root/COVID-Belgium-Dashboard/data/filtered_data/KMEANS.csv")

representatives_info = representatives_info[representatives_info["PROVINCE"].isin(representatives)]
representatives_info = representatives_info[["INFECTION_RATE", "HOSPITALISATION_RATE", "TEST_POS_PERCENTAGE"]].to_numpy()

kmeans = Kmeans("/root/COVID-Belgium-Dashboard/data/filtered_data/KMEANS.csv", 4, representatives_info)
kmeans.read_csv(["INFECTION_RATE", "HOSPITALISATION_RATE", "TEST_POS_PERCENTAGE"])
kmeans.start_clustering()
kmeans.results_to_csv("/root/COVID-Belgium-Dashboard/data/resulted_data/kmeans")