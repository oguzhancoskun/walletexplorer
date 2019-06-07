#!/usr/bin/python
import requests,re, MySQLdb

def connect():
        conn = MySQLdb.connect(host = "[DBENDPOINT]", port= [PORT], user = "[DBUSER]", passwd = "[DBPASS]", db = "[DBNAME]")
        cur = conn.cursor()
        return cur, conn

def save(market,wallet):
        cur,conn = connect()
        query = """INSERT INTO wallets(market,wallet) VALUES(%s,%s)"""
        values = (market,wallet)
        cur.execute(query,values)
        conn.commit()
        cur.close()
        conn.close()


markets = ['Poloniex.com', 'Kraken.com', 'Bittrex.com','Cex.io']

for i in markets:
    url2 = 'https://www.walletexplorer.com/wallet/%s/addresses?page=1'%(i)
    o = requests.get(url = url2)
    p = re.findall(r'Page\s+1\s+\/\s+(\w+)', str(o.content), re.I | re.U)
    for j in range(1,int(p[0]),1):
        url = 'https://www.walletexplorer.com/wallet/%s/addresses?page=%s'%(i,j)
        r = requests.get(url = url)
        x = re.findall(r'address\/(\w+)">', str(r.content), re.I | re.U)
	for k in x:
       	    save(i,k)
