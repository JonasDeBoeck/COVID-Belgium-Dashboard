import pandas as pd

df = pd.read_csv("data\original_files\\2021_BE_Region_Mobility_Report.csv")
# df = df[df['place_id']  == "ChIJl5fz7WR9wUcR8g_mObTy60c"]
df['sub_region_2'].mask(df['sub_region_2'] == 'Antwerp', 'Antwerpen', inplace=True)
df['sub_region_2'].mask(df['sub_region_2'] == 'East Flanders', 'OostVlaanderen', inplace=True)
df['sub_region_2'].mask(df['sub_region_2'] == 'Flemish Brabant', 'VlaamsBrabant', inplace=True)
df['sub_region_2'].mask(df['sub_region_2'] == 'Province of Namur', 'Namur', inplace=True)
df['sub_region_2'].mask(df['sub_region_2'] == 'Walloon Brabant', 'BrabantWallon', inplace=True)
df['sub_region_2'].mask(df['sub_region_2'] == 'West Flanders', 'WestVlaanderen', inplace=True)
df.to_csv("data\\filtered_data\\MOBILITY.csv")


