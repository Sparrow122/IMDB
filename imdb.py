import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
from collections import defaultdict

def get_data(url,number_of_pages):
    headers = {
    "User-Agent": 'Mozilla/5.0(Windows NT 6.1Win64x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 87.0 .4280 .141 Safari / 537.36 '}
    res = requests.get(url,headers)
    soup1 = BeautifulSoup(res.content,'html.parser')
    movie_rows_list = soup1.find_all('div',{"class":"lister-item mode-advanced"})
    next_page = soup1.find('a',{"class":"lister-page-next next-page"}).attrs['href']
    next_page = "https://www.imdb.com"+soup1.find('a',{"class":"lister-page-next next-page"}).attrs['href']
    print (next_page)
    save_data(movie_rows_list)
    if (number_of_pages == 0):
        return
    else:
        print (number_of_pages)
        return get_data(next_page,number_of_pages-1)
    

def save_data(movie_rows_list):
    for i in range(len(movie_rows_list)):
        if (movie_rows_list[i].select('h3 a')[0].get_text()):
            movie_details['Movie_Name'].append(movie_rows_list[i].select('h3 a')[0].get_text())
        else:
            movie_details['Movie_Name'].append([None])
        if (movie_rows_list[i].select('div[class="lister-item-content"] > p:nth-child(2) > span[class="runtime"]')):
            #print (movie_rows_list[i].select('div[class="lister-item-content"] > p:nth-child(2) > span[class="runtime"]')[0].get_text().split("min")[0].strip())
            movie_details['Duration_in_min'].append(movie_rows_list[i].select('div[class="lister-item-content"] > p:nth-child(2) > span[class="runtime"]')[0].get_text().split("min")[0].strip())
        else:
            movie_details['Duration_in_min'].append([None])
        if (movie_rows_list[i].select('div[class="lister-item-content"] > div > div:first-child > strong')[0].get_text()):
            movie_details['Rating'].append(movie_rows_list[i].select('div[class="lister-item-content"] > div > div:first-child > strong')[0].get_text())
        else:
            movie_details['Rating'].append([None])
        if (movie_rows_list[i].select('div[class="lister-item-content"] > p[class="sort-num_votes-visible"] > span:nth-child(2)')[0].get_text()):
            movie_details['Votes'].append(movie_rows_list[i].select('div[class="lister-item-content"] > p[class="sort-num_votes-visible"] > span:nth-child(2)')[0].get_text())
        else:
            movie_details['Votes'].append([None])
        if (movie_rows_list[i].select('div[class="lister-item-content"] > p[class="sort-num_votes-visible"] > span:last-child')[0].get_text().replace('$','').replace('M','')):
            movie_details['Gross_in_million_dollar'].append(movie_rows_list[i].select('div[class="lister-item-content"] > p[class="sort-num_votes-visible"] > span:last-child')[0].get_text().replace('$','').replace('M',''))
        else:
            movie_details['Gross_in_million_dollar'].append([None])
    return

movie_details = {'Movie_Name': [],
                    'Duration_in_min':[],
                    'Rating':[],
                    'Votes':[],
                    'Gross_in_million_dollar':[]}
start_url = 'https://www.imdb.com/search/title/?release_date=2018-01-01,2018-12-31&sort=num_votes,desc'
number_of_pages = int(input("Number of pages to scrape:",))
get_data(start_url,number_of_pages)
df = pd.DataFrame(movie_details)
writer = pd.ExcelWriter('D:\pythonprogs\movies.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Movies')
writer.save()
