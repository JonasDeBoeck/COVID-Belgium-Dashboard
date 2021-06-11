from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.settings import api_settings
import pandas as pd
import csv
import json

# Create your views here.
@api_view(('GET',))
def kmeans_results(request):
    data = {}
    with open("data\\resulted_data\kmeans\CLUSTER_METADATA.csv") as f:
        reader = csv.DictReader(f)
        metadata = []
        for row in reader:
            row_data = {"CLUSTER": row["CLUSTER"], "INFECTION_RATE": row["INFECTION_RATE"], "HOSPITALISATION_RATE": row["HOSPITALISATION_RATE"], "TEST_POS_PERCENTAGE": row["TEST_POS_PERCENTAGE"]}
            metadata.append(row_data)

        data["METADATA"] = metadata

    with open("data\\resulted_data\kmeans\CLUSTER_PROVINCES.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        province_data = []
        for row in reader: 
            row_data = {"PROVINCE": row["PROVINCE"], "INFECTION_RATE": row["INFECTION_RATE"], "HOSPITALISATION_RATE": row["HOSPITALISATION_RATE"], "TEST_POS_PERCENTAGE": row["TEST_POS_PERCENTAGE"], "CLUSTER": row["CLUSTER"]}
            province_data.append(row_data)

        data["PROVINCES"] = province_data

    res = json.dumps(data, ensure_ascii=False).encode("utf8")
    return HttpResponse(res, content_type="application/json")
