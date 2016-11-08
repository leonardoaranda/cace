import pandas as pd   



data = pd.read_csv('prospects_metrics.csv')
output = []

def perc(val):
	return float(str(val).replace('%',''))

def vis(val):
	try:
		val = str(val)
		v = 0
		if 'M' in val:
			return float(val.replace('M',''))*1000000
		elif 'K' in val:
			return float(val.replace('K',''))*1000
		else:
			v = float(val)
		return v
	except:
		return None

for i,row in data.iterrows():
	bounce = perc(row['bounce'])
	organic_search = perc(row['organic_search'])
	paid_search = perc(row['paid_search'])
	traffic_direct = perc(row['traffic_direct'])
	traffic_display = perc(row['traffic_display'])
	traffic_mail = perc(row['traffic_mail'])
	traffic_referrals = perc(row['traffic_referrals'])
	traffic_search = perc(row['traffic_search'])
	traffic_social = perc(row['traffic_social'])
	visits = vis(row['visits'])

	data = {
		'bounce' : bounce,
		'category' : row['category'],
		'category_rank' : float(str(row['category_rank']).replace(',','')),
		'company' :  row['company'],
		'country_rank' : float(str(row['country_rank']).replace(',','')),
		'global_rank' : float(str(row['global_rank']).replace(',','')),
		'organic_search' : organic_search,
		'paid_search' : paid_search,
		'phone' : row['phone'],
		'ppv' : row['ppv'],
		'time' : row['time'],
		'traffic_direct' : traffic_direct,
		'traffic_display' : traffic_display,
		'traffic_mail' :  traffic_mail,
		'traffic_referrals' : traffic_referrals,
		'traffic_search' : traffic_search,
		'traffic_social' : traffic_social,
		'url' : row['url'],
		'visits' : visits
	}
	output.append(data)


pd.DataFrame(output).to_csv('cace_metrics.csv',index=False)