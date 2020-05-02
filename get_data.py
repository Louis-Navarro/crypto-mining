from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import json


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

    print('Buying cost: ', end='')
    buying = int(input())

    print('Power: ', end='')
    power = int(input())
    energy = power * 24 * 365
    energy_cost = energy * 0.15

    print('Euros per year: ', end='')
    earned = int(input())
    profit = earned - energy_cost

    with open('data/data.json', 'w+') as fp:
        data = json.load(fp)
        if currency not in data:
            data[currency] = {}
        way = f'way{1 + data[currency]}'
        
        data[currency][way] = {
                'name': name,
                'buying_price (in €)': buying,
                'power (in kW)': power,
                'energy (in kWh/year)': energy,
                'energy_cost (in €)': energy_cost,
                'earned_per_year (in €)': earned,
                'potential_profit (in €)': profit
                }


def main():
    print('Fetch currencies ? (Y/[n]) : ', end='')
    fetch = input()

    if fetch.lower == 'Y':
        currencies = get_currencies()
    
        with open('data/currencies.json', 'w') as fp:
            json.dump(currencies, fp)
    
    while True:
        add_way()

if __name__ == '__main__':
    main()
