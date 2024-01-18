import requests
from bs4 import BeautifulSoup


def brandSecimi(url):
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0"}

    # * bağlantı kontrolü
    try:
        page = requests.get(url, headers=header)
        page.raise_for_status()  # İsteğin başarılı olup olmadığını kontrol eder
    except requests.exceptions.RequestException as e:
        print(f"İstek yapılırken hata oluştu: {e}")
        exit()

    soup = BeautifulSoup(page.text, 'html.parser')
    perfumess = soup.select_one(
        "#contentListing > div > div.listingHolder > div.filterArea > section:nth-child(5) > div > div.filterList").find_all(
        "div")
    brandDict = {"tümü": url}

    for perfume in perfumess:
        try:
            perfume_text = perfume.find("a").text.strip()
            perfume_link = perfume.find("a").get("href")

            brandDict[perfume_text] = perfume_link
        except AttributeError:
            print("Element bulunamadı")

    # brand isimlerinin bir listesini oluşturur
    brandnames = list(brandDict.keys())

    # Kategorileri numaralarıyla birlikte yazdırır
    for i, brand in enumerate(brandnames, start=1):
        print(f"{i} - {brand}")

    brand_choice = int(input("Numarası ile marka seçin: "))

    # Liste indekslerinin 0'dan başladığını unutmayın, bu yüzden brand_choice'den 1 çıkarırız
    chosenbrand = brandnames[brand_choice - 1]

    # Seçilen brandnın bağlantısını bulur
    chosenlink = brandDict[chosenbrand]

    if chosenbrand == "tümü":
        chosenlink = url + "?"
        return chosenlink
    else:
        # Kullanıcıdan brand seçmesini ister
        while True:
            try:
                brand_choice = int(input("Birden fazla seçmek istersen tekrar numara gir, istemezsen enter'a bas: "))
                chosenbrand = brandnames[brand_choice - 1]
                chosenlink += "-" + chosenbrand
                # burada m=Zara-Bargello gibi bir link oluşturuyor her ekstra brand için "-brand" şeklinde linke ekliyor
                if brand_choice > len(brandnames) or brand_choice < 1:
                    break
            except ValueError:
                break
        print(f"Seçtiğiniz marka {chosenbrand}, bağlantısı {chosenlink}")
        chosenlink += "&"
        return chosenlink
