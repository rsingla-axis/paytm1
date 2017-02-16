import requests
import re
import pymongo
import sys
import pycountry

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.CT      # attach to db
coll = db.location

city1=input('Enter city name: ')
fs_res = ['city','country',{'state':""},'country_code',{'type' : "city"}]
fs_res1 = ['city','state','country','country_code',{'type' : "city"}]
F_ress=[]

mapping = {country.name: country.alpha_2 for country in pycountry.countries}


def test_hotel_list():
	url='https://travel.paytm.com/api/hotels/v1/search-suggest/'+ city1 +'?suggest_version=2&client=web&channel=web&child_site_id=1&site_id=1&version=2'
	response = requests.get(url)
	jsonres = response.json()
	chars_to_remove = ['[', ']','\'']
	for r in jsonres['data'].values():
		for p in r[0].values()[2]:
			res = (str(p['p']))
			out = (res.translate(None, ''.join(chars_to_remove))).split(',')
			f_res=[{fs_res[i]:(((res.translate(None, ''.join(chars_to_remove))).split(',')[i])[1:])} if(len(out)<3) else {fs_res1[i]:(((res.translate(None, ''.join(chars_to_remove))).split(',')[i])[1:])} for i in range(len(out))]
			
			if((len(out))==2):
				f_res[0].update(fs_res[2])
				f_res[0].update(fs_res[4])
	
			else:
				f_res[0].update(fs_res1[4])
			
			
			F_ress.append({ k:v for i in range(len(f_res)) for k,v in f_res[i].items()})

		for r in F_ress:
			r['country_code'] = mapping.get(r['country'])					
	
	for i in range(len(F_ress)):
		print(str(i) + ":" + str(F_ress[i]))
	read = int(input("Enter your choice: "))
	coll.insert(F_ress[read])			
if __name__ == '__main__':
    test_hotel_list()


