import json
import re

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_currencies(num_page=1):
    driver = webdriver.Chrome()
    driver.get("https://coinmarketcap.com/fr/coins/views/all/")
    
    if num_page > 1:
        elem = driver.find_element_by_css_selector('button.cmc-button.cmc-button--color-default.wn9odt-0.bzWQIF')

        for _ in range(num_page - 1):
            elem.click()

    names = [elem.text for elem in driver.find_elements_by_xpath('//table/tbody/tr/td[2]/div/a')]

    driver.quit()

    return names


def add_way():
    print('Currency: ', end='')
    currency = input()

    if not currency:
        print('Goodbye!')
        quit()

    print('Name: ', end='')
    name = input()

    print('Buying cost (in $): ', end='')
    buying = float(input())

    print('Power (in W): ', end='')
    power = float(input()) / 1000
    energy = power * 24
    energy_cost = energy * 0.17

    print('Earnings per day (in $): ', end='')
    earned = float(input())
    profit = earned - energy_cost

    with open('data/data.json', 'r') as fp:
        data = json.load(fp)
        if currency not in data:
            data[currency] = {}
        way = f'way{1 + len(data[currency])}'
        
        data[currency][way] = {
                'Name': name,
                'Buying price (in $)': buying,
                'Power (in kW)': power,
                'Energy (in kWh/day)': energy,
                'Energy cost (in $/day)': energy_cost,
                'Earnings (in $/day)': earned,
                'Potential profit (in $/day)': profit
                }

        print(pd.DataFrame(data).iloc[-1])
        
        print('Do you want to write that information ? ([y]/N) : ', end='')
        write = input() != 'N'

    if write:
        with open('data/data.json', 'w') as fp:
            json.dump(data, fp)


def main():
    print('Fetch currencies ? (Y/[n]) : ', end='')
    fetch = input()

    if fetch == 'Y':
        currencies = get_currencies()
    
        with open('data/currencies.json', 'w') as fp:
            json.dump(currencies, fp)
    
    while True:
        add_way()

if __name__ == '__main__':
    main()
