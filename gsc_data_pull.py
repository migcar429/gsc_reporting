#!/usr/bin/env python

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

import httplib2
'''from oauth2client import client
from oauth2client import file
from oauth2client import tools'''

from time import sleep
from datetime import date, timedelta

import json
import csv

# Dates - change when necessary.
end_date = date.today() - timedelta(days=1)
start_date = end_date - timedelta(days=6)
start_date, end_date = str(start_date), str(end_date)

# Credentials and other necessary info.
service_account_location = '/path/to/txt/with/email'
key_file_location = '/path/to/secret'
scope = 'https://www.googleapis.com/auth/webmasters.readonly'
api_name = 'webmasters'
api_version = 'v3'

# Body of the http request to GSC API.
request = {
	#'aggregationType': 'byProperty',
	'startDate': start_date,
	'endDate': end_date
	}

# URLs to loop through for search analytics.
root_url = 'www.somewebsite.com'
url_list = [
	root_url+'subdirectory1/',
	root_url+'subdirectory2/',
	root_url+'subdirectory3/',
	root_url+'subdirectory4/',
	root_url+'subdirectory5/',
	root_url+'subdirectory6/',
	root_url+'subdirectory7/',
	root_url+'subdirectory8/',
	root_url+'subdirectory9/',
	root_url+'subdirectory10/',
	root_url+'subdirectory11/'
	]

def main():

	service = get_service(api_name, api_version, scope, key_file_location, service_account_location)
	
	#sitemap_list = service.sitemaps().list(siteUrl='https://www.somewebsite.com/').execute()
	#get_sitemap(service, sitemap_list)

	#with open('stuff.json', 'w') as outfile:
	#	json.dump(sitemap_list, outfile)
	
	
	data = get_search_analytics(service, url_list)

	#with open('stuff2.json', 'w') as outfile:
	#	json.dump(get_search_analytics(url_list), outfile)
	
	dump_to_csv(data)
	#print service.sitemaps().get(siteUrl='https://www.somewebsite.com', feedpath='https://www.somewebsite.com/comprehensivesitemap85709624/thr_dbl_tier4_zips_index').execute()


def get_service(api_name, api_version, scope, key_file_location, service_account_location):
	# Build service object. 1) read credentials from files, 2) build credentials object, 3) authorize with necessary http headers, 4) build service object
	service_account_email, key = read_credentials(service_account_location, key_file_location)

	credentials = SignedJwtAssertionCredentials(service_account_email, key, scope=scope)
	http_auth = credentials.authorize(httplib2.Http())
	
	service = build(api_name, api_version, http=http_auth)

	return service


def read_credentials(service_account_location, key_file_location):
	# Read credentials from files outside the .py
	f = open(service_account_location, 'r')
	service_account_email = f.read()
	f.close()

	f = open(key_file_location, 'r')
	key = f.read()
	f.close()

	return service_account_email, key


def get_sitemap(service, sitemap_list):

	all_sitemaps = []

	for sitemap in sitemap_list['sitemap']:
		
		all_sitemaps.append([
			sitemap['path'],
			sitemap['contents'][0]['indexed'], 
			sitemap['contents'][0]['type'], 
			sitemap['contents'][0]['submitted']
		])
	
	#sitemap = service.sitemaps().get(siteUrl = 'https://www.somewebsite.com', feedpath = 'http://www.somewebsite.com/comprehensivesitemap85709624/prof_act_0_49999').execute()

	print all_sitemaps
	return all_sitemaps


def get_search_analytics(service, url_list):
# Loop through url_list and get basic analytics. Store in a dict.

	#all_analytics = {}
	all_analytics = []

	'''for url in url_list:
		datapoint = service.searchanalytics().query(siteUrl=url, body=request).execute()

		all_analytics[url] = {}
		all_analytics[url]['impressions'] = datapoint['rows'][0]['impressions']
		all_analytics[url]['ctr'] = datapoint['rows'][0]['ctr']
		all_analytics[url]['position'] = datapoint['rows'][0]['position']
		sleep(0.5)'''

	all_analytics.append([
		'Directory',
		'Impressions',
		'Clicks',
		'CTR',
		'Position'
	])

	for url in url_list:
		datapoint = service.searchanalytics().query(siteUrl=url, body=request).execute()

		all_analytics.append([
			url,
			datapoint['rows'][0]['impressions'],
			datapoint['rows'][0]['clicks'],
			datapoint['rows'][0]['ctr'],
			datapoint['rows'][0]['position']
		])

		sleep(0.25)

	#print all_analytics
	return all_analytics


def dump_to_csv(data):

	with open('SomeWebsite SearchAnalytics {0} to {1}.csv'.format(start_date, end_date), 'w') as outfile:
		writer = csv.writer(outfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

		for line in data:
			writer.writerow(line)

	return None


if __name__ == '__main__':
	main()

