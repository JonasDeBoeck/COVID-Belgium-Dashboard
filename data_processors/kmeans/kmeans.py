import pandas as pd
from datetime import date

cases_df = pd.read_csv("data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv")
hosp_df = pd.read_csv("data/filtered_data/HOSP.csv")
tests_df = pd.read_csv("data/filtered_data/TESTS.csv")
metadata_df = pd.read_csv("data/filtered_data/METADATA.csv")

current_month = date.today().month 
if current_month == 1:
    current_month = 12
else:
    current_month -= 1
current_year = date.today().year

cases_df["DATE"] = pd.to_datetime(cases_df["DATE"])
cases_df = cases_df.reset_index(drop=True)
cases_df = cases_df[cases_df["DATE"].dt.month == current_month]
cases_df = cases_df[cases_df["DATE"].dt.year == current_year]

hosp_df["DATE"] = pd.to_datetime(cases_df["DATE"])
hosp_df = hosp_df.reset_index(drop=True)
hosp_df = hosp_df[hosp_df["DATE"].dt.month == current_month]
hosp_df = hosp_df[hosp_df["DATE"].dt.year == current_year]

tests_df["DATE"] = pd.to_datetime(cases_df["DATE"])
tests_df = tests_df.reset_index(drop=True)
tests_df = tests_df[tests_df["DATE"].dt.month == current_month]
tests_df = tests_df[tests_df["DATE"].dt.year == current_year]

columns = ["PROVINCE", "INFECTION_RATE", "HOSPITALISATION_RATE", "TEST_POS_PERCENTAGE"]
df = pd.DataFrame(columns=columns)

provinces = ["VlaamsBrabant", "WestVlaanderen", "OostVlaanderen", "Namur", "Luxembourg", "Limburg", "Liège", "Hainaut", "Brussels", "BrabantWallon", "Antwerpen"]

for province in provinces:
    cases_province = (cases_df[cases_df["REGION"] == province])
    hosp_province = (hosp_df[hosp_df["REGION"] == province])
    tests_province = (tests_df[tests_df["REGION"] == province])
    metadata_province = (metadata_df[metadata_df["REGION"] == province])

    province_df = pd.DataFrame({
        "PROVINCE": province,
        "INFECTION_RATE":(cases_province["NEW_CASES"].sum() / metadata_province.iloc[0]["POPULATION"]) * 100,
        "HOSPITALISATION_RATE": (hosp_province["NEW_IN"].sum() / cases_province["NEW_CASES"].sum()) * 100,
        "TEST_POS_PERCENTAGE": (tests_province["TESTS_ALL_POS"].sum() / tests_province["TESTS_ALL"].sum()) * 100
        }, index=[0])

    df = df.append(province_df)

df = df.reset_index(drop=True)

df.to_csv("data/filtered_data/KMEANS.csv")