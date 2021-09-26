from Crypto.PublicKey import RSA
from serpapi import GoogleSearch
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from base64 import b64encode
import requests
import datetime
import math

class Product:
    def __init__( self , data ):
        self.itemId = data['itemId']
        self.name = data['name'].encode("ascii", "ignore").decode()
        self.salePrice = data['salePrice']
        self.description = data['shortDescription'].encode("ascii", "ignore").decode()
        self.brandName = data['brandName'].encode("ascii", "ignore").decode()
        self.image = data['mediumImage']
        self.icon = data['thumbnailImage']


    @classmethod
    def catalog(cls):
        endpoint = "https://developer.api.walmart.com/api-proxy/service/affil/product/v2/taxonomy"
        headers = generateWalmartHeaders()
        response = requests.get(endpoint, headers=headers)
        #json_data = json.loads(response.text)
        data = response.json()
        # for item in data['items']:
        #     for k in item:
        #         if(isinstance(item[k],str)):
        #             item[k] = item[k].encode("ascii", "ignore").decode()
        print(data)

    @staticmethod
    def search_with_brand(cls, searchTerm, brand):
        endpoint = 'https://developer.api.walmart.com/api-proxy/service/affil/product/v2/search?query='+searchTerm+'&facet=on&facet.filter=brand:'+brand
        headers = generateWalmartHeaders()
        response = requests.get(endpoint, headers=headers)
        #json_data = json.loads(response.text)
        data = response.json()
        products = []
        for item in data['items']:
            products.append(cls(item))
        return(products)

    @classmethod
    def getOne(cls, productId):
        endpoint = 'https://developer.api.walmart.com/api-proxy/service/affil/product/v2/items/'+ productId
        headers = generateWalmartHeaders()
        response = requests.get(endpoint, headers=headers)
        #json_data = json.loads(response.text)
        data = response.json()
        return(cls(data))

    @classmethod
    def search(cls, searchTerm):
        endpoint = 'https://developer.api.walmart.com/api-proxy/service/affil/product/v2/search?query='+searchTerm+'&responseGroup=full'
        headers = generateWalmartHeaders()
        response = requests.get(endpoint, headers=headers)
        #json_data = json.loads(response.text)
        data = response.json()
        products = []
        for item in data['items']:
            products.append(cls(item))
        return(products)

    @staticmethod
    def search_with_category(cls, searchTerm, categoryId):
        endpoint = 'https://developer.api.walmart.com/api-proxy/service/affil/product/v2/search?query='+searchTerm+'&categoryId='+categoryId
        headers = generateWalmartHeaders()
        response = requests.get(endpoint, headers=headers)
        #json_data = json.loads(response.text)
        data = response.json()
        products = []
        for item in data['items']:
            products.append(cls(item))
        return(products)
# Walmart key shenanigans
with open('.\\flask_app\\models\\private-key.pem', 'r') as f:
    private_key = RSA.import_key(f.read())

def generateWalmartHeaders():
    hashList = {
        "WM_CONSUMER.ID": "af4d3436-0c76-4456-8133-ac1713dcb60c",
        "WM_CONSUMER.INTIMESTAMP": str(math.trunc(datetime.datetime.now().timestamp() * 1000)),
        "WM_SEC.KEY_VERSION": str(3)
    }
    sortedHashString = hashList["WM_CONSUMER.ID"]+'\n'+hashList["WM_CONSUMER.INTIMESTAMP"]+'\n'+hashList["WM_SEC.KEY_VERSION"]+'\n'
    byteArrayHash = bytearray(sortedHashString.encode())
    hash = SHA256.new(byteArrayHash)
    signer = pkcs1_15.new(private_key)
    signature = signer.sign(hash)
    signature_enc = b64encode(signature)
    result = {
        "WM_SEC.AUTH_SIGNATURE": signature_enc,
        "WM_CONSUMER.INTIMESTAMP": hashList["WM_CONSUMER.INTIMESTAMP"],
        "WM_CONSUMER.ID": hashList["WM_CONSUMER.ID"],
        "WM_SEC.KEY_VERSION": hashList["WM_SEC.KEY_VERSION"],
    }
    return result

class Product2:
    def __init__( self , data ):
        self.itemId = data['us_item_id']
        self.name = data['title'].encode("ascii", "ignore").decode()
        self.salePrice = data['primary_offer']['offer_price']
        # self.description = data['description'].encode("ascii", "ignore").decode()
        self.brandName = data['seller_name'].encode("ascii", "ignore").decode()
        self.image = data['thumbnail']
        self.icon = data['thumbnail']

    @classmethod
    def search(cls, searchTerm):
        params = {
            "engine": "walmart",
            "query": searchTerm,
            "api_key": "f7be645ddf5ae8e979913ad0f6a2584bb26c2478b02cace0adec0799f2d108a8"
        }   

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results['organic_results']
        print(organic_results)
        products = []
        for item in organic_results:
            products.append(cls(item))
        return(products)


# Product.catalog()
# products = Product.search('Baby Snacks')
# products = Product.trend()
# print(len(products))
# for item in products:
#     print('itemId', item.itemId)
#     print('name', item.name)
#     print('salePrice', item.salePrice)
#     print('description', item.description)
#     print('brandName', item.brandName)
#     print('image', item.image)