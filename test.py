#Los respectivos imports
import pandas as pd
import numpy as np
import json
from flare.data_science.features import domain_tld_extract

from pyparsing import col

file_path = './large_eve.json'

data = []
for line in open(file_path, 'r'):
    data.append(json.loads(line))


data_dns = []

for j in data:
    for i in j:
        try: 
            if 'DNS' in i or 'dns' in i:
                data_dns.append(j)
        except:
            pass


df = pd.json_normalize(data_dns)



key_list = ['dns.type',
'dns.id',
'dns.rrname',
'dns.rrtype',
'dns.tx_id',
'dns.rcode',
'dns.ttl',
'dns.rdata']

df = df.rename(columns= {'dns.type': 'dns_type', 'dns.id': 'dns_id', 'dns.rrname': 'dns_rrname', 'dns.rrtype': 'dns_rrtype', 'dns.tx_id': 'dns_tx_id', 'dns.rcode': 'dns_rcode', 'dns.ttl': 'dns_ttl', 'dns.rdata': 'dns_rdata'})

df_dns_A = df.query("dns_rrtype == 'A'")


df2 = df_dns_A.drop_duplicates(subset='dns_rrname', keep=False, ignore_index=True)


tld_list = []

print(df2.head())

for i in range(len(df2)):
    tld_list.append(domain_tld_extract(df2['dns_rrname'][i]))

df2['tld'] = tld_list



print(df2.head())