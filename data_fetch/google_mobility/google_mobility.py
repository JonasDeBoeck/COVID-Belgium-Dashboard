
from zipfile import ZipFile
import requests
import os

zipurl = "https://www.gstatic.com/covid19/mobility/Region_Mobility_Report_CSVs.zip"


with open("data/original_files/temp.zip", 'wb') as fd:
    r = requests.get(zipurl, stream=True)
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)

with ZipFile("data/original_files/temp.zip") as zip_file:
    for member in zip_file.namelist():
        if member == "2021_BE_Region_Mobility_Report.csv":
            zip_file.extract(member, path="data/original_files")

os.remove("data/original_files/temp.zip")
