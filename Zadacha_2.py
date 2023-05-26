import requests
import lxml
from bs4 import BeautifulSoup
import time
from datetime import datetime
coins_1=['eth']
result={}
tick=0
arr=[]
while True:
    html_res=requests.get('https://coinranking.com/ru').text
    block=BeautifulSoup(html_res, 'lxml')
    rows=block.find_all('tr', class_='table__row--full-width')
    # columns=block.find_all('')
    for row in rows:
        ticker=row.find('span', class_='profile__subtitle-name')
        percent=row.find('div', class_='change change--light')
        
        if percent:
            print("percent:", percent)
        if ticker:
            ticker=ticker.text.strip().lower()
            if ticker in coins_1:
                price = row.find("td", class_="table__cell--responsive")
                if price:
                    price = (float(price.find("div", class_="valuta--light").text\
                                .replace("$", "").replace(",", ".").replace(" ", "")\
                                .replace("\n", "").replace("\xa0", "")))
                result[ticker.lower()] = price
                tick=result['eth']
                
               
                arr.append(tick) # у нас есть лист который зафиксирует курс Эфериума каждый пять секунд.  
                print(tick)
                
                if len(arr)==720: # Каждый час длина массива будет равен 720, и тогда начинает проверить что было изменение курса 1% или больше 
                    # print("arr", arr) # мы можем получить весь список за последний час..

                    x=(max(arr)*100)/min(arr) # здесь подсчитаем процентное отношение
                    if x-100>=1: # если разница 1% или больше тогда 
                        now = datetime.now()
                        current_time = now.strftime("%D:%H:%M:%S") #зафиксируем время 
                        print(f'Changed ", {x-100},"%,  Eth interval: [{ max(arr) }, { min(arr) }], Time: {current_time}')
                    arr.clear() # И каждый час очистим наш массив
                time.sleep(5)




