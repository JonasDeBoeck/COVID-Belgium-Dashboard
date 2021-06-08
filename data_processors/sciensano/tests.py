import pandas as pd
from datetime import date

tests_df = pd.read_csv("data/original_files/COVID19BE_TESTS.csv")
tests_df = tests_df.dropna(subset=["DATE"])
tests_df = tests_df.drop(["REGION"], axis=1)
columns = ["DATE", "REGION", "TESTS_ALL", "TESTS_ALL_POS"]

df = pd.DataFrame(columns=columns)

tests_belgium = tests_df.groupby("DATE", as_index=False).sum()
tests_belgium["REGION"] = "Belgium"
print(tests_belgium)
df = df.append(tests_belgium)

provinces = ["VlaamsBrabant", "WestVlaanderen", "OostVlaanderen", "Namur", "Luxembourg", "Limburg", "Liège", "Hainaut", "Brussels", "BrabantWallon", "Antwerpen"]

for province in provinces:
    tests_province = (tests_df[tests_df["PROVINCE"] == province])
    tests_province = tests_province.rename(columns={"PROVINCE": "REGION"})
    print(df)
    print(tests_province)
    df = df.append(tests_province)

df.to_csv("data/filtered_data/TESTS.csv")