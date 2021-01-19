##### Imports #####
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import re, requests, io, time, random, string, pprint
from datetime import date
from credentials import email, password
from list_of_stocks import stock_list
from pymongo import MongoClient

# MongoDB
client = MongoClient()
db = client['stock_data']
collection = db.current_data

# pprint
pp = pprint.PrettyPrinter(indent=4)

driver = webdriver.Chrome('/home/corey/Desktop/SEI1019/unit_four/codealong/chromedriver') # open chrome
time.sleep(1)

def sign_in(email=email, password=password):
    driver.get('https://wallmine.com') # go to url in address bar
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/main/header/div/ul/li[1]/ul/li[3]/a').click() # Click on sign in
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="new_user"]/div[5]/div[1]/div[2]/a').click() # Click on sign in w/password
    if "We're glad you're back!" in driver.page_source: # this conditional checks that we're on the right page.
        print("On Sign in page!")
        driver.find_element_by_xpath('//*[@id="user_email"]').send_keys(email) # inputs email into email input field
        driver.find_element_by_xpath('//*[@id="user_password"]').send_keys(password) # inputs password into password field
        time.sleep(0.1)
        driver.find_element_by_xpath('//*[@id="new_user"]/div[5]/div[2]/div[1]/button').click()
        time.sleep(1)
    if 'Stock market overview' in driver.page_source:
        print("Sign In Successful")
    else:
       print("start over app")



def get_data(stock_list): # needs to be an array of objects, objects need stock_ticker and exchange as keys
    for i in range(len(stock_list)):
        each_stock = stock_list[i]
        print(f"{i}: {each_stock.get('stock_ticker')}, exchange: {each_stock.get('exchange')}")
        driver.get(f"http://wallmine.com/{each_stock.get('exchange')}/{each_stock.get('stock_ticker')}")

        # company_name 
        company_name = driver.find_element_by_xpath('/html/body/main/section/div[2]/div/div[1]/h1/div[2]/a').text
        # current_price
        current_price = driver.find_element_by_xpath('/html/body/main/section/div[3]/div/div/div/div/div[2]/div/div[1]/span[1]').text
        # percentage positive and negative percentages are different classes

        percentage = driver.find_element_by_xpath('/html/body/main/section/div[3]/div/div/div/div/div[2]/div/div[2]/div').text
        price_movement = True
        if driver.find_elements_by_class_name('badge.badge-success'):
            price_up = driver.find_elements_by_class_name('badge.badge-success')[0].text
            if price_up == percentage:
                print('price up')
        elif driver.find_elements_by_class_name('badge.badge-danger'):
            price_down = driver.find_elements_by_class_name('badge.badge-danger')[0].text
            if price_down == percentage:
                price_movement = False
                print('price down')
        # amount_changed
        amount_changed = float(driver.find_element_by_xpath('/html/body/main/section/div[3]/div/div/div/div/div[2]/div/div[1]/span[2]').text[1:])
        # market_cap
        check_market_cap = driver.find_element_by_xpath('/html/body/main/section/div[4]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[1]/td/span').text
        market_cap = 0
        if check_market_cap[-1] == 'B':
            market_cap = float(check_market_cap[1:-1]) * 1000000000
        elif check_market_cap[-1] == 'M':
            market_cap = float(check_market_cap[1:-1]) * 1000000
        elif check_market_cap[-1] == 'T':
            market_cap = float(check_market_cap[1:-1]) * 1000000000000
        else:
            market_cap = 'N/A'
        # enterprise_value
        check_enterprise_value = driver.find_element_by_xpath('/html/body/main/section/div[4]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[2]/td').text
        enterprise_value = 0
        if check_enterprise_value[-1] == 'B':
            enterprise_value = float(check_enterprise_value[1:-1]) * 1000000000
        elif check_enterprise_value[-1] == 'M':
            enterprise_value = float(check_enterprise_value[1:-1]) * 1000000
        elif check_enterprise_value[-1] == 'T':
            enterprise_value = float(check_enterprise_value[1:-1]) * 1000000000000
        else:
            enterprise_value = 'N/A'
        # ebitda
        check_ebitda = driver.find_element_by_xpath('/html/body/main/section/div[4]/div[1]/div[2]/div[1]/div[2]/table/tbody/tr[2]/td/span').text
        ebitda = 0
        if check_ebitda[-1] == 'B':
            ebitda = float(check_ebitda[1:-1]) * 1000000000
        elif check_ebitda[-1] == 'M':
            ebitda = float(check_ebitda[1:-1]) * 1000000
        elif check_ebitda[-1] == 'T':
            ebitda = float(check_ebitda[1:-1]) * 1000000000000
        else:
            ebitda = 'N/A'
        # income
        check_income = driver.find_element_by_xpath('/html/body/main/section/div[4]/div[1]/div[2]/div[1]/div[2]/table/tbody/tr[3]/td/span').text
        income = 0
        if check_income[-1] == 'B':
            income = float(check_income[1:-1]) * 1000000000
        elif check_income[-1] == 'M':
            income = float(check_income[1:-1]) * 1000000
        elif check_income[-1] == 'T':
            income = float(check_income[1:-1]) * 1000000000000
        else:
            income = 'N/A'
        # volume
        check_volume = driver.find_element_by_xpath('/html/body/main/section/div[4]/div[1]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td').text.split(' / ')
        volume_purchased = check_volume[0]
        volume_outstanding = check_volume[1]
        # relative_volume
        relative_volume = driver.find_element_by_xpath('/html/body/main/section/div[4]/div[1]/div[2]/div[2]/div[1]/table/tbody/tr[2]/td/span').text
        # print(volume_outstanding)
            # time.sleep(3)


    # Stock Object
        stock_object = {
        'company_name': company_name,
        'stock_ticker': each_stock.get('stock_ticker'),
        'exchange': each_stock.get('exchange'),
        'current_price': current_price,
        'percentage': percentage,
        'price_movement': price_movement,
        'amount_changed': amount_changed,
        'market_cap': market_cap,
        'enterprise_value': enterprise_value,
        'ebitda': ebitda,
        'volume': check_volume,
        'volume_purchased': volume_purchased,
        'volume_outstanding': volume_outstanding,
        'relative_volume': relative_volume,
        # 'date': date.today()
    }

        # pp.pprint(stock_object)
        # Insert Stock Object into database
        db.current_data.insert_one(stock_object)
        retrieve_stock = db.current_data.find_one({'stock_ticker': each_stock.get('stock_ticker')})
        pp.pprint(retrieve_stock)

sign_in(email, password)
get_data(stock_list)

