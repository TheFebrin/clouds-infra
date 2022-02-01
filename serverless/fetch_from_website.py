import bs4
import datetime
from google.cloud import firestore
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

URL = 'https://www.worldometers.info/coronavirus/'


def find_poland(tables):
    for table in tables:
        for element in table:
            for x in element:
                if isinstance(x, bs4.element.Tag):
                    href = x.get('href')
                    if href is not None and href.find('country/poland/') != -1:
                        return table


def get_data_from_table(table):
    data = []
    for element in table:
        try:
            if len(new_entry := element.text.strip()) > 0:
                data.append(new_entry)
        except:
            pass
    final_data = data[:15]

    # Handle different data displayed on the website
    if final_data[-3] == 'Europe' or final_data[-1].find(',') == -1:
        final_data.insert(3, '0')
        final_data.insert(5, '0')
        final_data.insert(7, '0')

    return final_data[:15]

def main(_request):
    if _request is not None:
        print('Got request: ', _request.get_json(), _request.args)

    req = Request(URL, headers=hdr)
    html = urlopen(req)
    soup = BeautifulSoup(html, "html.parser")
    global_data = soup.find_all("div", {"class": "maincounter-number"})
    global_data = [x.text.strip() for x in global_data]

    tables = soup.findChildren('table')[0].findChildren(['tr'])
    polish_table = find_poland(tables)
    if polish_table is None:
        data_dict = {
            'all_cases': 0,
            'country' : 'ERROR'
        }
    else:
        polish_data = get_data_from_table(polish_table)
        print(f'polish_data: {polish_data}')
        data_dict = {
            'all_cases': int(global_data[0].replace(',', '')),
            'deaths': int(global_data[1].replace(',', '')),
            'recovered': int(global_data[2].replace(',', '')),

            'total_cases_rank': int(polish_data[0].replace(',', '')),
            'country': polish_data[1],
            'total_cases': int(polish_data[2].replace(',', '')),
            'new_cases': int(polish_data[3].replace(',', '')),
            'total_deaths': int(polish_data[4].replace(',', '')),
            'new_deaths': int(polish_data[5].replace(',', '')),
            'total_recovered': int(polish_data[6].replace(',', '')),
            'new_recovered': int(polish_data[7].replace(',', '')),
            'active_cases': int(polish_data[8].replace(',', '')),
            'serious_critical': int(polish_data[9].replace(',', '')),
            'tot_cases_per_mln': int(polish_data[10].replace(',', '')),
            'deaths_per_mln': int(polish_data[11].replace(',', '')),
            'total_tests': int(polish_data[12].replace(',', '')),
            'tests_per_mln': int(polish_data[13].replace(',', '')),
            'population': int(polish_data[14].replace(',', '')),
        }

    
    print(data_dict)
    date: str = datetime.datetime.utcnow().strftime("%y-%m-%d-%H-%M-%S")
    print(f'Saving file: {date}')
    db = firestore.Client()
    doc_ref = db.collection('covid-data').document(date)
    doc_ref.set(data_dict)

    return 'DONE'


def display_data_from_db():
    db = firestore.Client()
    data_ref = db.collection(u'covid-data')

    for doc in data_ref.stream():
        print(u'{} => {}'.format(doc.id, doc.to_dict()))

if __name__ == '__main__':
    # display_data_from_db()
    main(None)