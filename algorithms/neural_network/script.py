import pandas as pd
import Utils
import matplotlib.pyplot as plt
import os
import shutil

province_metadata = pd.read_csv("data/filtered_data/METADATA.csv")
province_metadata = province_metadata.drop([province_metadata.index[1], province_metadata.index[2]])

data = pd.read_csv("data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv")

# for province in province_metadata.itertuples():
#     os.makedirs(f"data/resulted_data/neural_network/temp/{province[1]}", exist_ok = True)
#     province_data = (data[data["REGION"] == province[1]])
#     start_day = 0
#     end_day = 31
#     prev = 0

#     province_data = province_data.rename(columns={"DATE": "Data", "ACTIVE_CASES": "At", "CUMULATIVE_RECOVERED": "Rt", "CUMULATIVE_DEATHS": "Óbitos", "CUMULATIVE_CASES": "Confirmados"})
#     province_data = province_data.iloc[-33:-2]
#     print(province_data)
#     print(province_data)
#     for dLen in range(start_day, end_day):
#         ds = province_data[["At"]]
#         ini = ds[ds["At"] > 0]
#         nData = len(ini)
#         sl1 = dLen
#         sl = 31
#         learner, df = Utils.run_region(province[1], sl1, sl, province_data, province[2], step=14, is_SIR=True)
#         df.to_csv(f"data/resulted_data/neural_network/temp/{province[1]}/Subregions_Pred_{dLen}D_prev-{prev}-{province[1]}.csv")

#     Utils.run_unifica('Outputs', province[1], unify = True, crop = 14, MM = False, dia_ini = start_day, dia_fim = end_day - 1, recalc_rt=True, prev=prev, gen_graphs=False) 

shutil.rmtree("data/resulted_data/neural_network/temp/")