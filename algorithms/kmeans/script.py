import pandas as pd
import numpy as np
from kmeans import Kmeans
import os
import re 

wdir = os.getcwd()
wdir = re.sub(r'algorithms/kmeans', '', wdir)

representatives = ["WestVlaanderen", "Hainaut", "Brussels", "BrabantWallon"]

representatives_info = pd.read_csv(f"{wdir}/data/filtered_data/KMEANS.csv")

representatives_info = representatives_info[representatives_info["PROVINCE"].isin(representatives)]
representatives_info = representatives_info[["INFECTION_RATE", "HOSPITALISATION_RATE", "TEST_POS_PERCENTAGE"]].to_numpy()

kmeans = Kmeans(f"{wdir}/data/filtered_data/KMEANS.csv", 4, representatives_info)
kmeans.read_csv(["INFECTION_RATE", "HOSPITALISATION_RATE", "TEST_POS_PERCENTAGE"])
kmeans.start_clustering()
kmeans.results_to_csv(f"{wdir}/data/resulted_data/kmeans")