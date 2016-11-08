import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


prospects = []

for page in range(1,78):

	print 'Downloading page {0}'.format(page)

	uri = 'http://www.cace.org.ar/directorio-de-socios/page/{0}/'.format(page)
	html_doc = requests.get(uri).text.encode('ascii', 'ignore')
	soup = BeautifulSoup(html_doc, 'html.parser')

	i = 0
	for row in soup.find(id='listadoSocios').find_all('tr'):
		if i > 0:
			try:
				rows =  row.find_all('td')
				company = rows[1].string
				category = rows[2].string
				url = rows[3].find('a').string
				phone = rows[4].string
				if phone:
					phone = phone.strip()

				prospect = {
					'company' : company.strip(),
					'category' : category,
					'url' : url,
					'phone' : phone
				}
				prospects.append(prospect)
			except:
				print 'Warning, error'
		i+=1

pd.DataFrame(prospects).to_csv('prospects.csv',index=False)
