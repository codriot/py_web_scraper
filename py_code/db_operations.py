import sqlite3
from products import allProduct
from reviews import scrapeProductReview


def setProductsDB(url):
    conn = sqlite3.connect('my_database.db')
    df = allProduct(url)
    df.to_sql('desired_products', conn, if_exists="replace", index=False)
    conn.close()


def getSqliteLink():
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    siratipi = ["Yorum Adedine göre", "Akıllı Sıralama"]

    print("Sıralama tipini seçiniz")
    for i, name in enumerate(siratipi, start=1):
        print(f"{i}- {name}")

    siratipi_index = int(input("Select a product by number: "))
    if siratipi_index == 1:
        c.execute("SELECT * FROM desired_products ORDER BY CommentCount DESC")
    elif siratipi_index == 2:
        c.execute("SELECT * FROM desired_products ORDER BY CommentCount DESC , Star DESC")
    else:
        print("Hatalı giriş")
        return

    names = c.fetchall()
    # Tüm değerleri yazdır
    for i, name in enumerate(names, start=1):
        print(
            f"{i}- {name[0]}, Comment Count: {name[2]},Star: {name[3]} ")

    # Kullanıcıdan bir seçim yapmasını istiyorum
    product_index = int(input("Select a product by number: "))
    link = names[product_index - 1][1]  
    print(f"You chose {names[product_index][0]} with link {link}")
    conn.close()
    return link


def getProductsReview(url):
    conn = sqlite3.connect('my_database.db')
    rew = scrapeProductReview(url)
    rew.to_sql('review', conn, if_exists="replace", index=False)
    conn.close()
