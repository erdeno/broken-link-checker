#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup as bs
import requests
import re


def check_status(link):
    try:
        res = requests.get(link)
        if res.status_code==200:
            return 'SUCCESS'
        else:
            return 'ERROR'
    except:
        return 'ERROR'


def save_to_txt(data):
    with open('result.txt', 'a') as file:
        file.write(data)


def get_links_from_page(page, links):
    for l in page.find_all(attrs={'href': re.compile("http")}):
        link = l.get('href')
        if link not in links.keys():
            links[link] = check_status(link)
            data = f'{link} {links[link]} \n'
            save_to_txt(data)
            print(data)


if __name__ == '__main__':
    links = {}
    url = 'https://www.lambdatest.com/blog/'
    r = requests.get(url)
    data = r.text
    body = bs(data, 'html.parser').body
    running = True
    
    while running:
        get_links_from_page(body, links)
        next_page = body.select_one('div.pagination').find('a', text='Next ›')
        
        if next_page:
            url = next_page.get('href')
            r = requests.get(url)
            data = r.text
            body = bs(data, 'html.parser').body.select_one('.col-xs-12.col-md-10')
        else:
            running = False
    
    print('Execution finished you can check the result from result.txt file.')
