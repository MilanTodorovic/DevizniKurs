import random
import requests
import time
import datetime
import bs4
import DB

'''PROVERITI DA LI MOZE POST SA URLLIB.REQUEST.REQUEST'''
'''DODATI CHECKDATE TABELU ZA EFIKASNIJI KOD'''
'''DODATI DATUM U CHECKDATE'''


def nbs_parsing(days):

    myBrKursneListe=''
    myYear='2016'
    myExchangeRateListTypeID='1'
    myLang='lat'

    for j in range(-days,1):

        altDate = str((datetime.date.today()+datetime.timedelta(j)).strftime("%Y-%m-%d"))

        if DB.checkDate(altDate):
            continue

        lst_val = [[]]
        lst_head = []
        tag_num = 0
        i = 0
        myUrl = 'http://www.nbs.rs/kursnaListaModul/zaDevize.faces?date='
        myDate = str((datetime.date.today() + datetime.timedelta(j)).strftime("%d.%m.%Y."))

        myUrl += myDate + "&listno=" + myBrKursneListe + "&year=" + myYear + "&listtype=" + myExchangeRateListTypeID + "&lang=" + myLang
        print(myUrl)

        html = requests.post(myUrl).content
        soup = bs4.BeautifulSoup(html, "html.parser")
        headers = soup('th')
        tags = soup('td', {'class':'tableCell'})

        for head in headers:
            lst_head.append(head.text)

        for tag in tags:
            lst_val[i].append(tag.text)
            tag_num = tag_num + 1
            if tag_num%6 == 0:
                lst_val.append([])
                i = i +1

        # print(lst_val)
        DB.input_db(0,altDate,*lst_val)
        time.sleep(random.randrange(0,1))

def erste_parsing(days):

    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
                          'Connection':'keep-alive','X-Requested-With': 'XMLHttpRequest'})
    # cookies ={'_gat':'1','_ga':'GA1.2.508381398.1457976455',
    #       'wt3_eid':'%3B831800162300051%7C2145797550500348139%232145859247200562148',
    #       'wt3_sid':'%3B831800162300051'}
    s.get('https://www.erstebank.rs/rs/Pocetna/Kursna_lista')
    # s.get('https://www.erstebank.rs/resources/css/main.responsive.min.css?vn=2.20.0.0')
    # s.get('https://www.erstebank.rs/resources/js/lib/ext/mediaelement/js/v/mediaelement-and-player.min.js')
    # s.get('https://www.erstebank.rs/resources/js/main.responsive.min.js?vn=2.20.0.0')
    # s.get('https://www.erstebank.rs/resources/js/webtrekk.min.js?vn=2.20.0.0')
    # s.get('https://www.erstebank.rs/resources/js/lib/ext/safstats.js?vn=2.20.0.0')
    s.get('https://erstegroup01.webtrekk.net/831800162300051,820058945145099/wt?p=323,www_erstebank_rs.rs.pocetna.kursna_lista,1,1280x720,'
              '24,1,1458592472770,0,1280x193,0&tz=1&eid=2145797550500348139&one=0&fns=0&la=en&cg1=erstebank.rs&cg2=sr&cg3=Pocetna&cg4=Kursna_lista'
              '&cg9=rs&cg10=0784&cp1=Kursna%20lista%20Erste%20Banke%20%7C%20www.erstebank.rs&cs1=No&eor=1')

    for j in range(-days, 1):

        altDate = str((datetime.date.today()+datetime.timedelta(j)).strftime("%Y-%m-%d"))

        # if DB.checkDate(altDate):
        #     continue

        lst_val = [[]]
        lst_head = []
        tag_num = 0
        i = 0
        url = 'https://www.erstebank.rs/rs/Pocetna/Kursna_lista?_windowLabel=main0ExchangeRates&_pageLabel=CP' \
              '&_urlType=action&main0ExchangeRates_event=selectDate&main0ExchangeRates_pc=1' \
              '&main0ExchangeRates_action=module.fxrates.fxRates&_renderScope=portlet&main0ExchangeRates_date='
        myDate = str((datetime.date.today() + datetime.timedelta(j)).strftime("%d.%m.%Y"))
        # print(url)
        # print(s.cookies)
        url += myDate

        time.sleep(random.randrange(0, 1))

        html = s.get(url).content
        soup = bs4.BeautifulSoup(html, "html.parser")
        headers = soup('th')
        tags = soup('td')

        for head in headers:
            lst_head.append(head.text)

        for tag in tags:
            if not (tag.text).strip():
                continue
            lst_val[i].append(tag.text)
            tag_num = tag_num + 1
            if tag_num%9 == 0:
                lst_val.append([])
                i = i +1
        print(lst_val)
        DB.input_db(1,altDate,*lst_val)


def raiff_parsing(days):

    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
                          'Connection':'keep-alive','X-Requested-With': 'XMLHttpRequest'})
    s.get('https://www.raiffeisenbank.rs/pocetna.849.html')



    for j in range(-days,1):

        time.sleep(random.randrange(0,1))

        lst_val=[]
        lst=[[]]
        i=0
        myDate = str((datetime.date.today()+datetime.timedelta(j)).strftime("%Y-%m-%d"))
        myYear = myDate[:4]
        myMonth = myDate[5:7]
        myDay = myDate[8:]
        url = 'https://www.raiffeisenbank.rs/pocetna.849.html'
        data = {'date':myDate,
                'Id':'849',
                'ddl_kursnalista_dan':myDay,
                'ddl_kursnalista_mesec':myMonth,
                'ddl_kursnalista_godina':myYear,
                'txt_kursnalista_broj':'',
                'txt_kursnalista_brojgodina':myYear}
        print(myDate)
        html = s.post(url, data=data).content
        soup = bs4.BeautifulSoup(html, "html.parser")
        body = soup.find('tbody')
        tags = body.find_all('tr')

        for tag in tags:
            if not (tag.text).strip():
                continue
            lst_val.append(tag.text)

        for v in lst_val[1:]:
            k = v.split('\n')
            for m in k:
                # print(i)
                if m == '' or m is None:
                    continue
                lst[i].append(m)
            i+=1
            lst.append([])

        # print(lst_val)
        # print(lst)
        DB.input_db(2,myDate,*lst)


# DB.drop_tables()
DB.create_tables()
# DB.read_db()
# DB.checkDate('2016-03-26')

days = 365
nbs_parsing(days)
erste_parsing(days)
raiff_parsing(days)


# {'Accept':'text/html, */*; q=0.01',
# 'Accept-Encoding':'gzip, deflate, sdch',
# 'Accept-Language':'sr-RS,sr;q=0.8,en-US;q=0.6,en;q=0.4',
# 'Connection':'keep-alive',
# 'Cookie':'disclaimer=close; GPJSESSIONID=phdpWw2bg01WF0XTGlhtFKbGK1qvGHjjyXmgyKLr4nkqqNzQzrnf!-799165956; _ga=GA1.2.508381398.1457976455; wt3_eid=%3B831800162300051%7C2145797550500348139%232145858531700120704; wt3_sid=%3B831800162300051',
# 'Host':'www.erstebank.rs',
# 'Referer':'https://www.erstebank.rs/rs/Pocetna/Kursna_lista',
# 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
# 'X-Requested-With':'XMLHttpRequest'}
