#!/usr/bin/env python
# -*- coding: utf-8 -*-

def OCR_To_DataFrame(file_path):
    import json
    import base64
    import requests
    import pandas as pd

    with open(file_path, "rb") as f:
        img = base64.b64encode(f.read())

    URL = "https://bad5890da82043a0b2b9b8da10967f0e.apigw.ntruss.com/custom/v1/2952/595e2f18a0418462a86f146309a885fbf77dc7cd9f7e418079ff4d93b6bfb6ba/infer"

    KEY = "WEpmcml1dlpFVkdad1RCaEdxQWtoQUhpSmFpVkZsRlQ="

    headers = {
        "Content-Type": "application/json",
        "X-OCR-SECRET": KEY
    }

    data = {
        "version": "V1",
        "requestId": "sample_id",
        "timestamp": 0,
        "images": [
            {
                "name": "sample_image",
                "format": "png",
                "data": img.decode('utf-8')
            }
        ]
    }
    data = json.dumps(data)
    response = requests.post(URL, data=data, headers=headers)
    res = json.loads(response.text)

    jsonString = json.dumps(res, indent=4)

    dict = json.loads(jsonString)

    main = dict['images'][0]['fields']
    col = []
    data = []


    for i in range(0,len(main)) :
        col.append(main[i]['name'])
        data.append(main[i]['inferText'])

    default = 8
    datas = []
    for i in range(8, len(res['images'][0]['fields']), 6) :
        datas.append(data[0:default]+data[i:i+6])
        if(data[i]=='' or data[i]=='LAST ITEM') :
            break

    Test = pd.DataFrame(index=['SUPPLIER',
     'BUSUNIESSNUMBER',
     'OWNER',
     'ADDRESS',
     'TEL',
     'FAX',
     'OWNER_EMAIL',
     'ORDER_DATE',
     'PRODUCT',
     'PRODUCT_SIZE',
     'PRODUCT_UNIT',
     'PRODUCT_QUNTITY',
     'PRODUCT_UNITPRICE',
     'PRODUCT_PRICE',]).T

    for i in range(0, len(datas)) :
        Test.loc[i] = data[0:default] + datas[i][8:14]

    return Test