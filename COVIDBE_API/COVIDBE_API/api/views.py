from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework_csv import renderers as r
from rest_framework.settings import api_settings
import pandas as pd
import csv
import json

# Create your views here.
@api_view(('GET',))
def kmeans_results(request):
        with open("data\\resulted_data\kmeans\CLUSTER_METADATA.csv") as f:
            reader = csv.DictReader(f)    
            data = []  
            for row in reader:
                data.append(row)
            
            res = json.dumps(data)
            print(res)
            return HttpResponse(res, content_type="application/json")
