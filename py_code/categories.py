import requests
from bs4 import BeautifulSoup


def categories():
    url = "https://www.n11.com/parfum-ve-deodorant"
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0"}
    # * bağlantı kontrolü
    try:
        page = requests.get(url, headers=header)
        page.raise_for_status()  # Eğer bir hata varsa, hata fırlatır
    except requests.exceptions.RequestException as e:
        print(f"İstek yapılırken hata oluştu: {e}")
        exit()

    category_dict = {"Tümü": url}  # Kategorileri ve bağlantıları saklamak için bir sözlük oluşturur

    soup = BeautifulSoup(page.text, 'html.parser')
    perfumes = soup.find("li", class_="filterItem parent").find_all("ul")
    for perfume in perfumes:
        try:
            categoriestext = perfume.find("li").find("a").text.strip()  # Kategori adını alır
            categorieslink = perfume.find("li").find("a").get("href")  # Kategori bağlantısını alır
            category_dict[categoriestext] = categorieslink  # Kategori adını ve bağlantısını sözlüğe ekler
        except AttributeError:
            print("Element bulunamadı")

    # Kullanıcının bir kategori seçebilmesi için kategori adlarının bir listesini oluşturur
    category_names = list(category_dict.keys())

    # Kategori adlarını, indekslerini 1'den başlayacak şekilde yazdırır
    for i, category in enumerate(category_names, start=1):
        print(f"{i} - {category}")

    # Kullanıcıdan bir kategori numarası seçmesini ister
    category_choice = int(input("Bir kategori numarası seçin: "))

    # Liste indekslerinin 0'dan başladığını unutmayın, bu yüzden category_choice'den 1 çıkarırız
    chosen_category = category_names[category_choice - 1]

    # Seçilen kategorinin bağlantısını bulur
    chosen_link = category_dict[chosen_category]

    print(f"Seçtiğiniz kategori {chosen_category}, bağlantısı {chosen_link}")
    return chosen_link
