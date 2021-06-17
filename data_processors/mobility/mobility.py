import pandas as pd

df = pd.read_csv("data\original_files\\2021_BE_Region_Mobility_Report.csv")
df = df[df['place_id']  == "ChIJl5fz7WR9wUcR8g_mObTy60c"]
df.to_csv("data\\filtered_data\\MOBILITY.csv")


