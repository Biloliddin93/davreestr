import requests
import xmltodict
import onevizion
import json

with open('settings.json', 'rb') as PFile:
 password_data = json.loads(PFile.read().decode('utf-8'))



url = password_data['URL']
login = password_data['UserName']
password = password_data['Password']

APIURL =password_data['APIURL']
AUTHTOKENDAV =password_data['AUTHTOKENDAV']
URLS =password_data['URLS']




res=requests.get(URLS, auth=(login, password))



response = res.json()
for data in response:

    body = {'request_id': 'statement_doc',
            'cadastre_number': data['DAVR_CADASTRAL_NUMBER'],
            'cad_type': '0'}
    requ = requests.post(APIURL, data=body,
                             headers={'Authorization': AUTHTOKENDAV})

    getdav = requ.json()

    zapret = ''
    if getdav['data']['result_code'] == 0:
        zapret = 'Доступен'
    else:
        zapret = 'Запрет или арест'


    cbu_list_request = onevizion.Trackor(trackorType='DAVREESTR', URL=url, userName=login, password=password)

    cbu_list_request.update(data['TRACKOR_ID'],
                            fields={
                                'DAVR_INTEGRATION': 0,
                                'DAVR_CADASTRAL_STATUS': zapret,
                                'DAVR_SOATO': "17"+getdav['data']['region_id']+getdav['data']['area_id'],
                                'DAVR_STATUS_CODE': getdav['data']['result_code'],
                                'DAVR_CADASTRAL_NUMBER': getdav['data']['kadastr_no'],
                                'DAVR_NUMBER_OF_BUILDINGS': getdav['data']['count_objects'],
                                'DAVR_REGION': getdav['data']['region_name'],
                                'DAVR_AREA': getdav['data']['area_name'],


                                'DAVR_LAND_AREA': getdav['data']['area'],
                                'DAVR_LOCATION': getdav['data']['location'],
                                'DAVR_CADASTRAL_PRICE': getdav['data']['land_price'],

                                'DAVR_CERT_S_N': getdav['data']['cert_s_n'],
                                'DAVR_OBJECT_BAN': getdav['data']['err_text'],
                                'DAVR_OWNER': getdav['data']['subjects']['name'],


                            }
                            )























