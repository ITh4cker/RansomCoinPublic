#!/usr/bin/env python
# Copyleft 2018 Eireann Leverett of Concinnity Risks
#
#
# File name chasingcoin.py
# written by eireann.leverett@cantab.net
import requests
import json
import csv
from tqdm import tqdm

LIST_OF_ADDRESSES = []

with open('Ransomware.csv', 'r') as inputfile:
    coinreader = csv.reader(inputfile, delimiter=',',)
    for row in coinreader:
        if row[6] == 'BTC Address':
            LIST_OF_ADDRESSES.append(row[7])
inputfile.close()

# deduplicate the list
LIST_OF_ADDRESSES = list(set(LIST_OF_ADDRESSES))


with open('AccountsRecievingRansom.csv', 'w') as csvfile:
    RESULTS_WRITER = csv.writer(
        csvfile,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL)
    RESULTS_WRITER.writerow(['wallet',
                             'number of transactions',
                             'total BTC received',
                             'total BTC sent',
                             'final BTC balance'])
    for ADDRESS in tqdm(LIST_OF_ADDRESSES):
        s = requests.Session()
        s.auth = ('concinnity@cantab.net', '3158ef3d-593d-4c36-9c3f-c1ac5c1effda')
        try:
            with s.get('https://blockchain.info/rawaddr/' + ADDRESS, stream=True) as result:
                if result.status_code == 200:
                    data = result.json()
                    RESULTS_WRITER.writerow([data['address'],
                                             data['n_tx'],
                                             data['total_received']/100000000.00,
                                             data['total_sent']/1000000000.00,
                                             data['final_balance']/1000000000.00])
                else:
                    print('HTTP Response is: ' + str(result.status_code))
        except Exception as E:
            print(E)
csvfile.close()
