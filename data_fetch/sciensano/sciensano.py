import urllib
from urllib import request

cases_url = "https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv"
deaths_url = "https://epistat.sciensano.be/Data/COVID19BE_MORT.csv"
hospitalisations_url = "https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv"
tests_url = "https://epistat.sciensano.be/Data/COVID19BE_tests.csv"

urllib.request.urlretrieve(cases_url, "data/original_files/COVID19BE_CASES_AGESEX.csv")
urllib.request.urlretrieve(deaths_url, "data/original_files/COVID19BE_MORT.csv")
urllib.request.urlretrieve(hospitalisations_url, "data/original_files/COVID19BE_HOSP.csv")
urllib.request.urlretrieve(tests_url, "data/original_files/COVID19BE_TESTS.csv")