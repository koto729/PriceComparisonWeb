from lxml import etree
from datetime import date
import numpy as np
import requests
import re
import mysql.connector

#get today
today = date.today()

#link database
mydb = mysql.connector.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    password = "",
    database = "webscraper"
)
mycursor = mydb.cursor()


def product_url_list():
    #消毒藥水
    ztore_1 = 'https://www.ztore.com/tc/product/antiseptic-liquid-1000416-c5600'
    HKTVmall_1 = 'https://www.hktvmall.com/hktv/zh/main/%E6%BB%B4%E9%9C%B2/s/H1010002/%E8%B6%85%E7%B4%9A%E5%B7%BF%E5%A0%B4/%E8%B6%85%E7%B4%9A%E5%B8%82%E5%A0%B4/%E5%AE%B6%E5%B1%85%E6%B8%85%E6%BD%94%E7%94%A8%E5%93%81/%E6%BC%82%E7%99%BD%E6%B0%B4-%E6%B6%88%E6%AF%92%E5%8A%91/%E6%BB%B4%E9%9C%B2%E6%B6%88%E6%AF%92%E8%97%A5%E6%B0%B4-12L/p/H0888001_S_10003174'
    pns_1 = 'https://www.pns.hk/zh-hk/%E6%B6%88%E6%AF%92%E8%97%A5%E6%B0%B4/p/BP_198159'
    #洗潔精
    ztore_2 = 'https://www.ztore.com/tc/product/spring-fresh-lemon-dishwashing-liquid-1046038-c5590'
    HKTVmall_2 = 'https://www.hktvmall.com/hktv/zh/main/%E9%AB%98%E9%9C%B2%E6%BD%94/s/H1022001/%E8%B6%85%E7%B4%9A%E5%B7%BF%E5%A0%B4/%E8%B6%85%E7%B4%9A%E5%B8%82%E5%A0%B4/%E5%AE%B6%E5%B1%85%E6%B8%85%E6%BD%94%E7%94%A8%E5%93%81/%E5%BB%9A%E6%88%BF%E6%B8%85%E6%BD%94%E7%94%A8%E5%93%81/%E6%B4%97%E6%BD%94%E7%B2%BE-%E9%A3%9F%E7%89%A9%E6%B8%85%E6%BD%94%E5%8A%91/%E6%B8%85%E6%96%B0%E6%AA%B8%E6%AA%AC%E6%B4%97%E6%BD%94%E7%B2%BE-%E8%B6%85%E5%8B%81%E5%8E%BB%E6%B2%B9%E6%BC%AC%E5%A8%81%E5%8A%9B/p/H0888001_S_10133856'
    pns_2 = 'https://www.pns.hk/zh-hk/%E6%BB%B4%E6%BD%94%E6%B4%97%E6%BD%94%E7%B2%BE-%E6%B8%85%E6%96%B0%E6%AA%B8%E6%AA%AC800ml/p/BP_492105'
    #花生油
    ztore_3 = 'https://www.ztore.com/tc/product/supreme-peanut-oil-bonus-pack-1053069-c5384'
    HKTVmall_3 = 'https://www.hktvmall.com/hktv/zh/main/%E5%8D%97%E9%A0%86%E6%97%97%E8%89%A6%E5%BA%97/s/H1205001/%E8%B6%85%E7%B4%9A%E5%B7%BF%E5%A0%B4/%E8%B6%85%E7%B4%9A%E5%B8%82%E5%A0%B4/%E7%B1%B3-%E9%A3%9F%E6%B2%B9/%E9%A3%9F%E6%B2%B9/%E7%B2%9F%E7%B1%B3%E6%B2%B9-%E8%8A%B1%E7%94%9F%E6%B2%B9/%E5%88%80%E5%98%9C%E9%87%91%E8%A3%9D%E6%BF%83%E9%A6%99%E8%8A%B1%E7%94%9F%E6%B2%B9900MLX4/p/H0888001_S_10147229'
    pns_3 = 'https://www.pns.hk/zh-hk/%E9%87%91%E8%A3%9D%E6%BF%83%E9%A6%99%E8%8A%B1%E7%94%9F%E6%B2%B9-%E9%9A%A8%E6%A9%9F%E7%99%BC%E8%B2%A8/p/BP_452113'
    #米
    ztore_4 = 'https://www.ztore.com/tc/product/premium-jasmine-rice-1000531-c5373'
    HKTVmall_4 = 'https://www.hktvmall.com/hktv/zh/main/%E9%87%91%E6%BA%90%E7%B1%B3%E6%A5%AD/s/H1202001/%E8%B6%85%E7%B4%9A%E5%B7%BF%E5%A0%B4/%E8%B6%85%E7%B4%9A%E5%B8%82%E5%A0%B4/%E7%B1%B3-%E9%A3%9F%E6%B2%B9/%E7%B1%B3/%E6%B3%B0%E5%9C%8B%E5%8F%8A%E6%9D%B1%E5%8D%97%E4%BA%9E%E9%A6%99%E7%B1%B3/%E9%A0%82%E4%B8%8A%E8%8C%89%E8%8E%89%E9%A6%99%E7%B1%B3-8%E5%85%AC%E6%96%A4-%E9%87%91%E8%B1%A1%E9%87%91%E8%B1%A1%E7%89%8C%E9%A6%99%E7%B1%B3%E7%B1%B3%E7%85%AE%E9%A3%9F%E7%85%AE%E9%A3%AF%E7%85%B2%E4%BB%94%E9%A3%AF/p/H0888001_S_10016911'
    pns_4 = 'https://www.pns.hk/zh-hk/%E9%A0%82%E4%B8%8A%E8%8C%89%E8%8E%89%E9%A6%99%E7%B1%B3/p/BP_115992'
    #生抽
    ztore_5 = 'https://www.ztore.com/tc/product/premium-soy-sauce-1021372#query=%E7%94%9F%E6%8A%BD'
    HKTVmall_5 = 'https://www.hktvmall.com/hktv/zh/main/%E6%9D%8E%E9%8C%A6%E8%A8%98/s/H1028001/%E8%B6%85%E7%B4%9A%E5%B7%BF%E5%A0%B4/%E8%B6%85%E7%B4%9A%E5%B8%82%E5%A0%B4/%E8%AA%BF%E5%91%B3-%E9%86%AC%E6%96%99/%E8%B1%89%E6%B2%B9-%E8%A0%94%E6%B2%B9/%E7%94%9F%E6%8A%BD-%E9%A0%AD%E6%8A%BD/%E7%89%B9%E9%AE%AE%E7%94%9F%E6%8A%BD-%E5%84%AA%E6%83%A0%E8%A3%9D/p/H0888001_S_10014663'
    pns_5 = 'https://www.pns.hk/zh-hk/%E7%89%B9%E9%AE%AE%E7%94%9F%E6%8A%BD%E4%B8%89%E6%94%AF%E8%A3%9D/p/BP_372731'
    #衛生紙
    ztore_6 = 'https://www.ztore.com/tc/product/4d-deluxe-toilet-roll-4ply-baby-soft-full-case-single-roll-8001510-c5106'
    HKTVmall_6 = 'https://www.hktvmall.com/hktv/zh/main/Vinda/s/H1066001/%E8%B6%85%E7%B4%9A%E5%B7%BF%E5%A0%B4/%E8%B6%85%E7%B4%9A%E5%B8%82%E5%A0%B4/%E9%87%8D%E9%87%8F%E7%B4%9A%E6%8E%A8%E4%BB%8B/%E7%B4%99%E5%93%81-%E5%8D%B3%E6%A3%84%E5%93%81/%E5%8E%9F%E7%AE%B127%E5%8D%B7-4D-Deluxe-4%E5%B1%A4%E7%AB%8B%E9%AB%94%E5%A3%93%E8%8A%B1%E8%A1%9B%E7%94%9F%E7%B4%99%E5%96%AE%E5%8D%B7%E8%A3%9D-%E7%B4%99%E5%B7%BE%E5%BB%81%E7%B4%99%E7%84%A1%E9%A6%99%E6%A3%89%E6%9F%94%E8%A7%B8%E6%84%9F%E7%B6%B2%E5%BA%97%E7%8D%A8%E5%AE%B6/p/H0888001_S_P10135583'
    pns_6 = 'https://www.pns.hk/zh-hk/%E7%B6%AD%E9%81%944d%E7%AB%8B%E9%AB%94%E5%A3%93%E8%8A%B14%E5%B1%A4%E8%A1%9E%E7%94%9F%E7%B4%9927%E5%8D%B7%E8%A3%9D-%E5%8E%9F%E7%AE%B1/p/BP_350573'
    #洗衣液
    ztore_7 = 'https://www.ztore.com/tc/product/anti-bacteria-conc-liquid-detergent-6001989-c5604'
    HKTVmall_7 = 'https://www.hktvmall.com/hktv/zh/main/%E8%8A%B1%E7%8E%8B%E5%AE%98%E6%96%B9%E6%97%97%E8%89%A6%E5%BA%97/s/H0638001/%E8%B6%85%E7%B4%9A%E5%B7%BF%E5%A0%B4/%E8%B6%85%E7%B4%9A%E5%B8%82%E5%A0%B4/%E5%AE%B6%E5%B1%85%E6%B8%85%E6%BD%94%E7%94%A8%E5%93%81/%E6%B4%97%E8%A1%A3%E7%94%A8%E5%93%81/%E6%B4%97%E8%A1%A3%E6%B6%B2/%E5%84%AA%E6%83%A0%E5%AD%96%E8%A3%9D-%E6%8A%97%E8%8F%8C%E8%B6%85%E6%BF%83%E7%B8%AE%E6%B4%97%E8%A1%A3%E6%B6%B2/p/H0888001_S_10136554A'
    pns_7 = 'https://www.pns.hk/zh-hk/%E6%8A%97%E8%8F%8C%E6%B4%97%E8%A1%A3%E6%B6%B2-2-2l-%E5%84%AA%E6%83%A0%E8%A3%9D/p/BP_401503'

    #create array to save url
    product_url = np.array([["消毒藥水",ztore_1,HKTVmall_1,pns_1],
                            ["洗潔精",ztore_2,HKTVmall_2,pns_2],
                            ["花生油",ztore_3,HKTVmall_3,pns_3],
                            ["米",ztore_4,HKTVmall_4,pns_4],
                            ["生抽",ztore_5,HKTVmall_5,pns_5],
                            ["衛生紙",ztore_6,HKTVmall_6,pns_6],
                            ["洗衣液",ztore_7,HKTVmall_7,pns_7]])
    return(product_url)

def get_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    respose = requests.get(url,headers=headers)
    respose.encoding = "utf8"
    page_text = respose.text
    tree = etree.HTML(page_text)
    return tree

def scraper_ztore(url,type):
    supermaket_name = "ZTORE"
    product_name = get_page(url).xpath('//*[@id="detail"]/div[3]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/div/div/span/text()')[0]
    product_price = get_page(url).xpath('//*[@id="detail"]/div[1]/div[2]/div[4]/div/span[1]/text()')
    if len(product_price) >= 2:
        product_price = get_page(url).xpath('//*[@id="detail"]/div[1]/div[2]/div[4]/div/span[1]/text()')[1]
        product_price = float(product_price)
    else:
        product_price = get_page(url).xpath('//*[@id="detail"]/div[1]/div[2]/div[4]/div/span[1]/text()')[0]
        product_price = re.findall("\d+\.\d+|\d+", product_price)
        product_price = float(product_price[0])

    insertdatabase(type, supermaket_name, product_name, product_price)   
    return(supermaket_name+" "+product_name+"  $"+str(product_price))

def scraper_HKTVmall(url,type):
    supermaket_name = "HKTVmall"
    product_name = get_page(url).xpath('//*[@id="breadcrumb"]/div[2]/ul/li[2]/h1/text()')[0]
    product_price = get_page(url).xpath('//*[@id="mainWrapper"]/div/div[3]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div[2]/span/text()')[0]
    #extract number
    product_price = re.findall("\d+\.\d+", product_price)
    product_price = float(product_price[0])

    insertdatabase(type, supermaket_name, product_name, product_price)  
    return(supermaket_name+" "+product_name+"  $"+str(product_price))

def scraper_pns(url,type):
    supermaket_name = "PARKNSHOP"
    product_name = get_page(url).xpath('/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[3]/pns-product-summary/div/div[1]/a/text()')[0]
    product_name = product_name+" "+get_page(url).xpath('/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[3]/pns-product-summary/div/div[2]/h1/text()')[0]
    product_name = product_name+" "+get_page(url).xpath('/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[3]/pns-product-summary/div/div[3]/text()')[0]
    product_price = get_page(url).xpath('/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[3]/pns-product-summary/div/div[4]/div[1]/pns-product-price/span/text()')[0]
    
    #extract number
    product_price = re.findall("\d+\.\d+", product_price)
    product_price = float(product_price[0])

    insertdatabase(type, supermaket_name, product_name, product_price)  
    return(supermaket_name+" "+product_name+"  $"+str(product_price))

def insertdatabase(type, supermarket, product_name, price):

    sql = "INSERT INTO productprice (type_id, supermarket_id, product_name, price, date) VALUES ((SELECT id FROM type WHERE name = %s), (SELECT id FROM supermarket WHERE name = %s), %s, %s, CURRENT_DATE)"
    val = (type, supermarket, product_name, price)

    mycursor.execute(sql, val)

    mydb.commit()
query = "SELECT type_id, email, price FROM pricealerts"
mycursor.execute(query)

rows = mycursor.fetchall()

def send_simple_message(email, price, name):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox6e852debb374456a8125cfe97bf44cda.mailgun.org/messages",
		auth=("api", "04442fdf271e2321b72f5ba9d20dc6cf-6b161b0a-d812351c"),
		data={"from": "Price Comparison Website <ko.wingto.11@gmail.com",
			"to": 'User <'+email+'>',
			"subject": "Price Alerts of Price Comparison Website",
			"text": 'The price of the '+name+' you set a price alert for has reached your desired price of HK$ '+str(price)+'. Hurry up and make your purchase now!'})

for row in rows:
    type_id, email, price = row
    query = "SELECT * FROM productprice WHERE type_id = %s AND price <= %s AND date = (SELECT MAX(date) FROM productprice);"
    mycursor.execute(query, (type_id, price,))
    results = mycursor.fetchall()
    if results:
          print(email)
          send_simple_message(email, price, results[0][3])
    else:
        print("The condition is not met.")

        
if __name__ == "__main__":
    product_url = product_url_list()
    savefile = open("scraperdata.txt", "a",encoding='UTF-8')
    for x in range(len(product_url)):
        savefile.write("----------------------------------------------------\n")
        try:
            savefile.write(str(today)+"\n")
            savefile.write(str(scraper_ztore(product_url[x][1],product_url[x][0]))+"\n")
            savefile.write(str(scraper_HKTVmall(product_url[x][2],product_url[x][0]))+"\n")
            savefile.write(str(scraper_pns(product_url[x][3],product_url[x][0]))+"\n")
        except:
            print("sold")
        savefile.write("----------------------------------------------------\n")
    savefile.close()



    """
    for x in range(len(product_url)):
        print("----------------------------------------------------")
        print("scraper_date :", today)
        print("")
        scraper_ztore(product_url[x][0])
        scraper_HKTVmall(product_url[x][1])
        scraper_pns(product_url[x][2])
        print("----------------------------------------------------")
    """



