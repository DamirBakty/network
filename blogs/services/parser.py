import requests
from bs4 import BeautifulSoup
import json


def get_page(url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    return soup

link = "https://tengrinews.kz"
def parse():
    dump_data = {}
    arr = []
    for num in range(2,10): # число страниц которых собираемся парсить, в одной странице по 15 новостей где то
        parsed_html = get_page(link+'/read/page/' + str(num))
        a_href = parsed_html.find_all("a",{"class":"tn-link"})

        for i in a_href:
            try:
                parsed_html1 = get_page(link + i.get('href'))
                title = parsed_html1.find("h1", {"class" : "tn-content-title"}).getText()
                data = parsed_html1.find("article", {"class" : "tn-news-text"}).find_all("p")
                data_list = []

                for text in data:
                    if text.getText():
                        data_list.append(text.getText())
                dump_data["title"] = title
                dump_data["text"] = data_list[0]
                arr.append(dump_data)
            except:
                pass
            dump_data = {}
    return arr


a = parse()


with open('new.json', 'w') as file:
    json.dump(a, file, ensure_ascii=False)
