import requests
import os
import json

def extract_data(product):
    response = requests.get(product)
    response_dict = json.loads(response.text)
    response_str = json.dumps(response_dict,sort_keys=True, indent=4)
    return response_str
    
#Fetch details of products from REST API
celphones = "https://api.bestbuy.com/v1/products((categoryPath.id=pcmcat209400050001))?apiKey=?=100&format=json"
computers = "https://api.bestbuy.com/v1/products((categoryPath.id=abcat0501000))?apiKey=?=100&format=json"
laptops = "https://api.bestbuy.com/v1/products((categoryPath.id=abcat0502000))?apiKey=?&format=json"

#Define URL for Flume to send data 
flume_url = 'http://0.0.0.0:5140'

#Function call for cellphones
celphone_str = extract_data(celphones)
requests.post(flume_url, data=celphone_str)

#Function call for Desktops
computers_str = extract_data(computers)
requests.post(flume_url, data=computers_str)

#Function call for Desktops
laptops_str = extract_data(laptops)
requests.post(flume_url, data=laptops_str)