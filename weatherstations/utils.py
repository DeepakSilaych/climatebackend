
import requests
import time


def thing_data(thing_id):
    access_id = 'lX1d9akADFVLiYhB'
    access_key = 'NsKeyQDu9zgbED9KINEeYhIvRzbcSr1VKtDhbTMaUQMlAtPA8sOyjDm8Q85CBH9d'
    url = 'https://app.aurassure.com/-/api/iot-platform/v1.1.0/clients/10082/applications/16/things/data'

    now = int(time.time())
    from_time = now - 24 * 60 * 60

    payload = {
        'data_type': 'raw',
        'aggregation_period': 0,
        'parameters': ['us_mb'],
        'parameter_attributes': [],
        'things': [thing_id],
        'from_time': from_time,
        'upto_time': now
    }

    response = requests.post(url, json=payload, headers={
        'Access-Id': access_id, 
        'Access-Key': access_key,
        'Content-Type': 'application/json'
    })

    return response.json()
        
def things_list():
    access_id = 'lX1d9akADFVLiYhB'
    access_key = 'NsKeyQDu9zgbED9KINEeYhIvRzbcSr1VKtDhbTMaUQMlAtPA8sOyjDm8Q85CBH9d'
    url = 'https://app.aurassure.com/-/api/iot-platform/v1.1.0/clients/10684/applications/16/things/list'

    response = requests.get(url, headers={
        'Access-Id': access_id,
        'Access-Key': access_key,
        'Content-Type': 'application/json'
    })

    response_data = response.json()
    sensor_list = [
        {
            'id': sensor['id'],
            'name': sensor['name'],
            'latitude': sensor['latitude'],
            'longitude': sensor['longitude'],
            'address': sensor['address']
        } for sensor in response_data['things']
    ]

    return sensor_list