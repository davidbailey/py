import pandas as pd
import re
	//checked = input[(input['_raw'].str.contains(name, case=False))]

names = ['name1','name2']

for name in names:
	infile = name + '.csv'
	outfile = 'success-' + name + '.csv'
	input = pd.read_csv(infile, sep=',')
	checked = input
	if not checked.empty:
		success = checked[(checked['_raw'].str.contains('EventCode=4624'))]
		success.index = range(0,len(success))
		failure = checked[(checked['_raw'].str.contains('EventCode=4625'))]
		failure.index = range(0,len(failure))
		get_address = lambda x: re.findall('(Source Network Address:\\t)(.*?)(\\r)',x)[0][1]
		success['ip'] = success._raw.apply(get_address)
		failure['ip'] = failure._raw.apply(get_address)
		get_user = lambda x: re.findall('(Security ID:\\t)(.*?)(\\r)',x)[0][1]
		success['user'] = success._raw.apply(get_user)
		get_user2 = lambda x: re.findall('(Security ID:\\t)(.*?)(\\r)',x)[1][1]
		success['user2'] = success._raw.apply(get_user2)
		get_logontype = lambda x: re.findall('(Logon Type:\\t)(.*?)(\\r)',x)[0][1]
		success['logontype'] = success._raw.apply(get_logontype)
		failure['user'] = failure._raw.apply(get_user)
		success_csv = pd.DataFrame([success._time,success.ip,success.user,success.user2,success.logontype]).transpose()
		failure_csv = pd.DataFrame([failure._time,failure.ip])
		success_csv.to_csv(outfile)
		failure_csv.to_csv("failure.csv")
