import pandas as pd
from datetime import date

cases_df = pd.read_csv("data/original_files/COVID19BE_CASES_AGESEX.csv")
cases_df = cases_df.dropna(subset=["DATE"])
deaths_df = pd.read_csv("data/original_files/COVID19BE_MORT.csv")
deaths_df = deaths_df.dropna(subset=["DATE"])

columns = ["DATE", "REGION", "NEW_CASES", "CUMULATIVE_CASES", "NEW_RECOVERED", "CUMULATIVE_RECOVERED", "NEW_DEATHS", "CUMULATIVE_DEATHS", "ACTIVE_CASES"]

df = pd.DataFrame(columns=columns)
dates = pd.date_range(start="2020-03-01", end=date.today())

new_cases_belgium = cases_df.groupby("DATE", as_index=False).sum()
new_cases_belgium = new_cases_belgium.rename(columns={"CASES": "NEW_CASES"})
new_cases_belgium["REGION"] = "Belgium"
new_cases_belgium["DATE"] = pd.to_datetime(new_cases_belgium["DATE"])
missing_dates = dates.difference(new_cases_belgium["DATE"])
dates_df = pd.DataFrame({"DATE": missing_dates, "REGION": "Belgium", "NEW_CASES": 0})
new_cases_belgium = new_cases_belgium.append(dates_df)
new_cases_belgium = new_cases_belgium.sort_values(by="DATE")
new_cases_belgium["CUMULATIVE_CASES"] = new_cases_belgium["NEW_CASES"].cumsum()

new_deaths_belgium = deaths_df.groupby("DATE", as_index=False).sum()
new_deaths_belgium = new_deaths_belgium.rename(columns={"DEATHS": "NEW_DEATHS"})
new_deaths_belgium["DATE"] = pd.to_datetime(new_deaths_belgium["DATE"])
missing_dates = dates.difference(new_deaths_belgium["DATE"])
dates_df = pd.DataFrame({"DATE": missing_dates, "NEW_DEATHS": 0})
new_deaths_belgium = new_deaths_belgium.append(dates_df)
new_deaths_belgium = new_deaths_belgium.sort_values(by="DATE")
new_deaths_belgium["CUMULATIVE_DEATHS"] = new_deaths_belgium["NEW_DEATHS"].cumsum()

new_cases_belgium["NEW_RECOVERED"] = 0

for index, row in new_cases_belgium.iterrows():
    if index > 20:
        new_cases_belgium.iloc[index, 4] = new_cases_belgium.iloc[index - 21, 1] - new_deaths_belgium.iloc[index - 21, 1]
new_cases_belgium["CUMULATIVE_RECOVERED"] = new_cases_belgium["NEW_RECOVERED"].cumsum()

belgium_df = new_cases_belgium.join(new_deaths_belgium.set_index("DATE"), on="DATE")

df = df.append(belgium_df)
df = df.reset_index(drop=True)

provinces = ["VlaamsBrabant", "WestVlaanderen", "OostVlaanderen", "Namur", "Luxembourg", "Limburg", "Liège", "Hainaut", "Brussels", "BrabantWallon", "Antwerpen"]
for province in provinces:
    new_cases_province = (cases_df[cases_df["PROVINCE"] == province])
    new_cases_province = new_cases_province.groupby("DATE", as_index=False).sum()
    new_cases_province["REGION"] = province
    new_cases_province = new_cases_province.rename(columns={"CASES": "NEW_CASES"})
    new_cases_province["DATE"] = pd.to_datetime(new_cases_province["DATE"])
    missing_dates = dates.difference(new_cases_province["DATE"])
    dates_df = pd.DataFrame({"DATE": missing_dates, "REGION": province, "NEW_CASES": 0})
    new_cases_province = new_cases_province.append(dates_df)
    new_cases_province = new_cases_province.sort_values(by="DATE")
    new_cases_province["CUMULATIVE_CASES"] = new_cases_province["NEW_CASES"].cumsum()
    new_cases_province["NEW_RECOVERED"] = 0
    for index, row in new_cases_province.iterrows():
        if index > 13:
            new_cases_province.iloc[index, 4] = new_cases_province.iloc[index - 14, 1]
    new_cases_province["CUMULATIVE_RECOVERED"] = new_cases_province["NEW_RECOVERED"].cumsum()
    new_cases_province["NEW_DEATHS"] = 0
    new_cases_province["CUMULATIVE_DEATHS"] = 0
    df = df.append(new_cases_province)
    df = df.reset_index(drop=True)

df["ACTIVE_CASES"] = df["CUMULATIVE_CASES"] - df["CUMULATIVE_RECOVERED"] - df["CUMULATIVE_DEATHS"]

df.to_csv("data/filtered_data/CASES_RECOVERED_DEATHS_ACTIVE.csv")