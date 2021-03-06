import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

sites = [
	'garbarino.com'
]

def metrics(site):
	url = 'https://www.similarweb.com/website/'+site
	r = requests.get(url,timeout=10)
	html_doc = r.text.encode('ascii', 'ignore')
	soup = BeautifulSoup(html_doc, 'html.parser')

	data = {
		'global_rank' : metric(global_rank,soup),
		'country_rank' : metric(country_rank,soup),
		'category_rank' : metric(category_rank,soup),
		'bounce' : metric(bounce,soup),
		'ppv' : metric(ppv,soup),
		'time' : metric(time,soup),
		'visits' : metric(visits,soup),
		'traffic_direct' : metric(traffic_direct,soup),
		'traffic_referrals' : metric(traffic_referrals,soup),
		'traffic_search' : metric(traffic_search,soup),
		'traffic_social' : metric(traffic_social,soup),
		'traffic_mail' : metric(traffic_mail,soup),
		'traffic_display' : metric(traffic_display,soup),
		'organic_search' : metric(organic_search,soup),
		'paid_search' : metric(paid_search,soup)
	}

	return data

def metric(f,s):
	try:
		return f(s)
	except:
		return None


def global_rank(soup):
	div = soup.find_all(attrs={'data-view':'WebsitePageModule.Views.RankingView','data-rank-subject':'Global'})[0]
	value = div.find_all(attrs={'class':'rankingItem-value js-countable'})[0].get('data-value')
	return value

def country_rank(soup):
	div = soup.find_all(attrs={'data-view':'WebsitePageModule.Views.RankingView','data-rank-subject':'Country'})[0]
	value = div.find_all(attrs={'class':'rankingItem-value js-countable'})[0].get('data-value')
	return value

def category_rank(soup):
	div = soup.find_all(attrs={'data-view':'WebsitePageModule.Views.RankingView','data-rank-subject':'Category'})[0]
	value = div.find_all(attrs={'class':'rankingItem-value js-countable'})[0].get('data-value')
	return value

def bounce(soup):
	return soup.find_all(attrs={'data-type':'bounce'})[0].find_all(attrs={'class':'engagementInfo-value u-text-ellipsis js-countValue'})[0].string

def ppv(soup):
	return soup.find_all(attrs={'data-type':'ppv'})[0].find_all(attrs={'class':'engagementInfo-value u-text-ellipsis js-countValue'})[0].string

def time(soup):
	return soup.find_all(attrs={'data-type':'time'})[0].find_all(attrs={'class':'engagementInfo-value u-text-ellipsis js-countValue'})[0].string

def visits(soup):
	return soup.find_all(attrs={'data-type':'visits'})[0].find_all(attrs={'class':'engagementInfo-valueNumber js-countValue'})[0].string

def traffic_direct(soup):
	return soup.find_all(attrs={'class':'trafficSourcesChart-item direct'})[0].find_all(attrs={'class':'trafficSourcesChart-value'})[0].string

def traffic_referrals(soup):
	return soup.find_all(attrs={'class':'trafficSourcesChart-item referrals'})[0].find_all(attrs={'class':'trafficSourcesChart-value'})[0].string

def traffic_search(soup):
	return soup.find_all(attrs={'class':'trafficSourcesChart-item search'})[0].find_all(attrs={'class':'trafficSourcesChart-value'})[0].string

def traffic_social(soup):
	return soup.find_all(attrs={'class':'trafficSourcesChart-item social'})[0].find_all(attrs={'class':'trafficSourcesChart-value'})[0].string

def traffic_mail(soup):
	return soup.find_all(attrs={'class':'trafficSourcesChart-item mail'})[0].find_all(attrs={'class':'trafficSourcesChart-value'})[0].string

def traffic_display(soup):
	return soup.find_all(attrs={'class':'trafficSourcesChart-item display'})[0].find_all(attrs={'class':'trafficSourcesChart-value'})[0].string

def organic_search(soup):
	return soup.find_all(attrs={'class':'searchPie-text searchPie-text--left  '})[0].find_all(attrs={'class':'searchPie-number'})[0].string

def paid_search(soup):
	return soup.find_all(attrs={'class':'searchPie-text searchPie-text--right  '})[0].find_all(attrs={'class':'searchPie-number'})[0].string


prospects_metrics = []

prospects = pd.read_csv('prospects.csv').sample(frac=1)
x = 1

for i,row in prospects.iterrows():
	try:
		url = row['url'].replace('http://www.','').replace('www.','').replace('https://','').replace('http://','').replace('WWW.','').split('/')[0].lower()
		data = metrics(url)

		print 'Downloading {0} , #{1}'.format(url,x)

		data['url'] = url
		data['company'] = row['company']
		data['category'] = row['category']
		data['phone'] = row['phone']

		prospects_metrics.append(data)
	except:
		print 'Warning, Error'
	x+=1

pd.DataFrame(prospects_metrics).to_csv('prospects_metrics.csv',index=False)