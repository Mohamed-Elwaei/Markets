import json
import pprint
from flask import Flask, render_template, url_for
import pandas as pd
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/NASDAQ')
def NASDAQ():
    urla='https://markets.businessinsider.com/index/components/nasdaq_100'
    urlb='https://markets.businessinsider.com/index/components/nasdaq_100?p=2'
    df=pd.read_html('https://markets.businessinsider.com/index/components/nasdaq_100')[0]
    df2=pd.read_html('https://markets.businessinsider.com/index/components/nasdaq_100?p=2')[0]
    dftmp=pd.concat([df,df2],axis=0).reset_index(drop=True)
    res1=requests.get(urla)
    soup1=BeautifulSoup(res1.text,'html.parser')
    tds=soup1.find_all('td')
    res1=requests.get(urlb)
    soup1=BeautifulSoup(res1.text,'html.parser')
    tds=tds+soup1.find_all('td')
    a_tags=[]
    for td in tds:
        tmp=td.find_all('a',href=True)
        if tmp:a_tags.append(tmp[0]['href'][8:].split('-')[0].upper())
    symbol_df=pd.DataFrame({'Symbol':a_tags})     
    new_df=pd.concat([symbol_df,dftmp],axis=1)
    
    return render_template('NASDAQ.html', df=new_df,Index='NASDAQ')
@app.route('/FTSE100')
def FTSE():
    urla='https://markets.businessinsider.com/index/components/ftse_100'
    urlb='https://markets.businessinsider.com/index/components/ftse_100?p=2'
    df=pd.read_html('https://markets.businessinsider.com/index/components/ftse_100')[0]
    df2=pd.read_html('https://markets.businessinsider.com/index/components/ftse_100?p=2')[0]
    dftmp=pd.concat([df,df2],axis=0).reset_index(drop=True)
    res1=requests.get(urla)
    soup1=BeautifulSoup(res1.text,'html.parser')
    tds=soup1.find_all('td')
    res1=requests.get(urlb)
    soup1=BeautifulSoup(res1.text,'html.parser')
    tds=tds+soup1.find_all('td')
    a_tags=[]
    for td in tds:
        tmp=td.find_all('a',href=True)
        if tmp:a_tags.append(tmp[0]['href'][8:].split('-')[0].upper())
    symbol_df=pd.DataFrame({'Symbol':a_tags})     
    new_df=pd.concat([symbol_df,dftmp],axis=1)
    return render_template('NASDAQ.html', df=new_df,Index='FTSE 100')

@app.route('/DOW')
def DOW():
    url='https://markets.businessinsider.com/index/components/dow_jones'
    df=pd.read_html('https://markets.businessinsider.com/index/components/dow_jones')[0]
    result=requests.get(url)
    soup=BeautifulSoup(result.text,'html.parser')
    tds=soup.find_all('td')
    result=requests.get(url)
    soup=BeautifulSoup(result.text,'html.parser')
    a_tags=[]
    for td in tds:
        tmp=td.find_all('a',href=True)
        if tmp:a_tags.append(tmp[0]['href'][8:].split('-')[0].upper())
    symbol_df=pd.DataFrame({'Symbol':a_tags})     
    new_df=pd.concat([symbol_df,df],axis=1)
    print(new_df)
    return render_template('NASDAQ.html', df=new_df,Index='DOW')

@app.route('/SANDP/<int:pnum>')
def S_AND_P(pnum):
    url=f'https://markets.businessinsider.com/index/components/s&p_500?p={pnum}'
    print(url)
    df=pd.read_html(f'https://markets.businessinsider.com/index/components/s&p_500?p={pnum}')[0]
    result=requests.get(url)
    soup=BeautifulSoup(result.text,'html.parser')
    tds=soup.find_all('td')
    result=requests.get(url)
    soup=BeautifulSoup(result.text,'html.parser')
    a_tags=[]
    for td in tds:
        tmp=td.find_all('a',href=True)
        if tmp:a_tags.append(tmp[0]['href'][8:].split('-')[0].upper())
    symbol_df=pd.DataFrame({'Symbol':a_tags})     
    new_df=pd.concat([symbol_df,df],axis=1)
    return render_template('S&P.html', df=new_df,Index='S&P 500')


@app.route('/Info/<symbol>')
def Info(symbol):
    url = f'https://finance.yahoo.com/quote/{symbol}/key-statistics/'
    headers = {"User-Agent":"Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table=soup.find_all('table')[0]
    table=table.find('thead').find('tr').find_all('th')
    columns=[i.get_text() for i in table]
    columns[1]='C'+columns[1].split('C')[1]
    df=pd.read_html(soup.prettify(),skiprows=0, flavor='bs4')
    df=[d.set_index(d.columns[0]) for d in df]
    Validation_measure=df[0]
    h2s=soup.find_all('h2',attrs={'class':'Pt(20px)'})
    h3s=soup.find_all('h3',attrs={'class':'Mt(20px)'})
    h3s=[h3.get_text() for h3 in h3s]
    h2s=[h2.get_text() for h2 in h2s]

    titles=[]
    tables=[]
    for i in range(len(h3s)):
        titles.append(h3s[i])
        tables.append(df[i+1])
    
    Trading_Info_titles=titles[0:3]
    Financial_highlights_titles=titles[3:]
    Trading_Info=tables[0:3]
    Financial_highlights=tables[3:]
    print(Validation_measure)
    # return 'kkkkkk'
    return render_template('info.html',symbol=symbol,
                           Validation_measure=Validation_measure,
                           Trading_Info_titles=Trading_Info_titles,
                           Financial_highlights_titles=Financial_highlights_titles,
                           Trading_Info=Trading_Info,
                           Financial_highlights=Financial_highlights)
@app.route('/Crypto/<p>')
def Crypto(p):
    import requests
    if p==1:url = 'https://cryptoslate.com/coins/'
    else:url=f'https://cryptoslate.com/coins/page/{p}/'
    
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.get(url, headers=header)

    df = pd.read_html(r.text)[0]
    df.fillna('NA')
    df=df.set_index('#')
    for i,row in df.iterrows():
        for x in row:
            print(x)
        break   
    return render_template('Crypto.html',df=df,p=p,p_int=int(p))


@app.route('/cryptocurrency/<name>')
def cryptocurrency(name):
    from requests import Request, Session, get
    
    'Credit: https://gist.github.com/SrNightmare09/c0492a8852eb172ebea6c93837837998'
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest' # Coinmarketcap API url

    parameters = { 'slug': f'{name.lower()}', 'convert': 'USD' } # API parameters to pass in for retrieving specific cryptocurrency data

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'cb27b6a1-9bd5-4915-85c1-29db0bd7f603'
    } # Replace 'YOUR_API_KEY' with the API key you have recieved in the previous step

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    info = json.loads(response.text)['data']
    id=list(info.keys())[0]
    pprint.pprint(info[id])
    for i in info[id]:
        print(i)
    return render_template('cryptocurrency.html', info=info[id],keys=list(info[id].keys()),quoteskeys=list(info[id]['quote']['USD'].keys()))

@app.route('/ETFs')
def ETFS():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.by import By
    options = Options()
    options.add_argument('--headless')
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\chromedriver.exe', options=options)
    
    driver.get("https://www.cnbc.com/funds-and-etfs/")
    ActionChains(driver).scroll_by_amount(0, 200).perform()

    titles=driver.find_elements(By.TAG_NAME,'h3')
    titles=[title.text for title in titles]

    dfs=pd.read_html(driver.page_source)
    for df in dfs:
        df=df.set_index('SYMBOL')

    title_with_df=dict()
    for i in range(len(titles)):
     title_with_df[titles[i]]=dfs[i]  
        

    driver.quit()
    return render_template('ETFs.html',title_with_df=title_with_df)

@app.route('/ETF/<symbol>')
def ETF(symbol):
    url=f'https://www.cnbc.com/quotes/{symbol}'
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')
    divs=soup.find_all('div',attrs={'class': 'Summary-subsection'})
    key_stats=divs[0]
    labels_ks=key_stats.find_all('span',attrs={'class': 'Summary-label'})
    vals_ks=key_stats.find_all('span',attrs={'class': 'Summary-value'})
    vals_ks=[i.text for i in vals_ks]
    labels_ks=[i.text for i in labels_ks]
    events_stats=divs[1]
    labels_events=events_stats.find_all('span',attrs={'class': 'Summary-label'})
    vals_events=events_stats.find_all('span',attrs={'class': 'Summary-value'})
    vals_events=[i.text for i in vals_events]
    labels_events=[i.text for i in labels_events]
    title=[]
    title.append(soup.find('h1').find('span',attrs={'class':'QuoteStrip-name'}).text)
    title.append(soup.find('h1').find('span',attrs={'class':'QuoteStrip-symbolAndExchange'}).text)
    return render_template('ETF_Info.html',labels_ks=labels_ks,
                           vals_events=vals_events,
                           vals_ks=vals_ks,
                           labels_events=labels_events,symbol=symbol,title=title)
    
@app.route('/ETF_Sector/<sector>')
def ETF_Sector(sector):
    url=f'https://www.cnbc.com/{sector}/'   
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.by import By
    url=f'https://www.cnbc.com/sector-etfs/'   
    options = Options()
    options.add_argument('--headless')
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\chromedriver.exe', options=options)
    driver.get(url)
    ActionChains(driver).scroll_by_amount(0, 200).perform()
    df=pd.read_html(driver.page_source)[0]
    cols=list(df.columns)
    title=sector.split('-')
    print(title)
    if len(title)==3:title=title[1:]
    title[0]=title[0].capitalize()
    title=title[0]+' ETFs'
    print(cols)
    return render_template('ETF_Sector.html',df=df,columns=cols,title=title)
if __name__=='main':
    app.run(debug=True)