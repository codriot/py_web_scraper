import requests
from bs4 import BeautifulSoup
from star_enum import Star
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def allProduct(url):
    df = firstFivePageScrape(url)
    f = othersPageScrape(url)
    df = pd.concat([df, f])
    return df


def firstFivePageScrape(url):
    options = Options()
    options.add_argument("--headless=new")  # Arka planda çalıştır
    options.add_argument("--disable-gpu")  # GPU kullanma
    options.add_argument('--ignore-certificate-errors')  # SSL sertifika hatalarını yoksay
    options.add_argument('--log-level=3')  # Sadece hata loglarını göster

    products_list = []
    scrollPauseTime = 0.2
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    lastheight = driver.execute_script("return document.body.scrollHeight")
    print(f'\r yükleniyor : 0', end='', flush=True)
    while True:
        for i in range(0, lastheight, 300):  # Her seferinde 200 piksel kaydır
            driver.execute_script("window.scrollTo(0, {});".format(i))
            time.sleep(scrollPauseTime)  # Scroll arası bekle

        # Yeni scroll yüksekliğini hesapla ve son scroll yüksekliği ile karşılaştır
        newheight = driver.execute_script("return document.body.scrollHeight")
        if newheight == lastheight:
            break
        lastheight = newheight
    print(f'\r yükleniyor : 5', end='', flush=True)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(1)  # Sayfanın yüklenmesini bekle
    getProduct(products_list, soup)
    df = pd.DataFrame(products_list, columns=['Name', 'Link', 'CommentCount', 'Star'])  # DataFrame oluştur
    return df


def othersPageScrape(url):
    products_list = []
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0"}

    s = requests.Session()  # Bir session başlat
    s.headers.update(header)  # Header'ı güncelle
    counter = 6  # Sayfa sayacı
    while True:
        try:
            print(f'\r yükleniyor : {counter * 2}', end='', flush=True)
            URL = f'{url}pg={counter}'  # URL'yi oluştur
            counter = counter + 1  # Sayacı arttır
            try:
                page = s.get(URL)
                page.raise_for_status()  # İsteğin başarılı olup olmadığını kontrol et
            except requests.exceptions.RequestException as e:
                print(f"İstek yapılırken hata oluştu: {e}")
                exit()
            soup = BeautifulSoup(page.text, 'html.parser')
            products = soup.find('div', id='view').find('ul').find_all('li')
            pagination = soup.find('div', class_='pagination').find('a', class_='next navigation')
            if len(products) < 1 or pagination is None:  # Eğer ürün kalmadıysa veya sonraki sayfa tuşu yoksa
                break
            getProduct(products_list, soup)
        except Exception as e:
            print('bitti', e)
            break
    df = pd.DataFrame(products_list, columns=['Name', 'Link', 'CommentCount', 'Star'])  # DataFrame oluştur
    print()
    return df


def getProduct(productslist: list, soup: BeautifulSoup):
    products = soup.find('div', id='view').find('ul').find_all('li')  # Ürünleri bul

    for i in range(len(products)):
        productsName = products[i].find('h3', class_='productName').text.strip()  # Ürün adını bul
        productsLink = products[i].find('a', class_='plink').get('href')  # Ürün linkini bul
        try:  # yorum yoksa None dönsün
            productsCommentCount = products[i].find('div', class_='proDetail').find('div', class_='ratingCont').find(
                "span", class_="ratingText").text.strip().replace("(", "").replace(")", "").replace(".", "").replace(
                ",", "")  # Yorum sayısını bul
            productsCommentCount = int(productsCommentCount)  # Yorum sayısını integer'a çevir
        except AttributeError:
            productsCommentCount = 0
        try:
            productsStar = products[i].find('div', class_='proDetail').find('div', class_='ratingCont').find(
                'span').get('class')  # Ürün yıldızını bul
            if productsStar is not None:
                if isinstance(productsStar,
                              list):  # Eğer productsStar bir liste ise("rating","r60") tarzında aldığı için
                    productsStar = ' '.join(productsStar)  # Listeyi string'e çevir
                    productsStar = productsStar.replace(" ", "")  # Boşlukları kaldır
            if productsStar in Star.__members__:  # Eğer productsStar, Star enum'ının üyelerinden biriyse
                productsStar = float(Star[productsStar].value)
        except AttributeError:
            productsStar = None
        productslist.append((productsName, productsLink, productsCommentCount, productsStar))
