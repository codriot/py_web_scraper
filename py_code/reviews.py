from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from star_enum import Star
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
import pandas as pd


def scrapeProductReview(url):
    def scrapeProduct(drivers: webdriver.Chrome):
        drivers.get(drivers.current_url)
        soup = BeautifulSoup(drivers.page_source, 'html.parser')
        reviewerslist = soup.find('div', class_='holder').find('ul').find_all('li')

        def getreview(val: int):
            # Yorum yapanın adını çek
            reviewername = reviewerslist[val].find('span', class_='userName').text.strip()

            # Yorumu çek
            review_text = reviewerslist[val].find('p').text

            # Yorum tarihini çek
            reviewdate = reviewerslist[val].find('span', class_='commentDate').text.strip()

            # Yıldız sayısını çek
            productStar = reviewerslist[val].find('div', class_='ratingCont').find('span').get('class')

            if productStar is not None:
                productStar = ' '.join(productStar)
                productStar = productStar.replace(" ", "")
            if productStar in Star.__members__:
                productStar = float(Star[productStar].value)
            else:
                productStar = None

            listAdd = (reviewername, review_text, productStar, reviewdate)
            return listAdd

        reviewerlist = []  # Yorum listesi oluştur
        for i in range(len(reviewerslist)):  # Her bir yorum için
            reviewerlist.append(getreview(i))  # Yorumu listeye ekle

        if not reviewerlist:  # Eğer liste boşsa
            print("No elements found")
        else:
            print(reviewerlist)
            return reviewerlist

    options = Options()
    options.add_argument("--headless=new")  # Arka planda çalıştır
    options.add_argument("--disable-gpu")  # GPU kullanma
    options.add_argument('--ignore-certificate-errors')  # SSL sertifika hatalarını yoksay
    options.add_argument('--log-level=3')  # Sadece hata loglarını göster

    driver = webdriver.Chrome(options=options)
    driver.get(url + "#unf-review")
    review = []
    while True:
        time.sleep(3)
        scraped_product = scrapeProduct(driver)
        if scraped_product in review:
            continue
        review.extend(scraped_product)
        if len(review) >= 100:
            review = review[:100]  # ilk 100 yorumu al
            break
        try:
            wait = WebDriverWait(driver, 10)
            button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.next.navigation")))  # Sonraki sayfa butonunu bul
            driver.execute_script("arguments[0].click();", button)  # Butona tıkla
        except NoSuchElementException:
            print("No more pages to navigate.")  # Daha fazla sayfa yok
            break
        except TimeoutException:
            print(
                "Timeout waiting for next page button to become clickable.")  # Buton tıklanabilir olana kadar beklerken zaman aşımı
            break
        except ElementClickInterceptedException:
            print(
                "Element is not clickable due to another element overlaying it.")  # Başka bir element butonun üzerini kapattığı için tıklanamıyor
            break
        
    df = pd.DataFrame(review,columns=['Name', 'rewiew', 'Star', 'Date'])  # DataFrame oluştur
    return df
