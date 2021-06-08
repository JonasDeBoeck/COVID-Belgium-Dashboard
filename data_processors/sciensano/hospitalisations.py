import pandas as pd
from datetime import date

hosp_df = pd.read_csv("data/original_files/COVID19BE_HOSP.csv")
hosp_df = hosp_df.dropna(subset=["DATE"])
hosp_df = hosp_df.drop(["NR_REPORTING", "TOTAL_IN", "TOTAL_IN_RESP", "TOTAL_IN_ECMO", "NEW_OUT", "REGION"], axis=1)
columns = ["DATE", "REGION", "TOTAL_IN_ICU", "NEW_IN"]

df = pd.DataFrame(columns=columns)

hosp_belgium = hosp_df.groupby("DATE", as_index=False).sum()
hosp_belgium["REGION"] = "Belgium"

df = df.append(hosp_belgium)

provinces = ["VlaamsBrabant", "WestVlaanderen", "OostVlaanderen", "Namur", "Luxembourg", "Limburg", "Liège", "Hainaut", "Brussels", "BrabantWallon", "Antwerpen"]

for province in provinces:
    hosp_province = (hosp_df[hosp_df["PROVINCE"] == province])
    hosp_province = hosp_province.rename(columns={"PROVINCE": "REGION"})
    df = df.append(hosp_province)

df = df.reset_index(drop=True)
df.to_csv("data/filtered_data/HOSP.csv")