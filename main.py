import sys

sys.path.append('py_code')
import py_code.categories as categories
import py_code.brand as brand
import py_code.db_operations as scrapeProducts


def main():
    link = categories.categories()
    link = brand.brandSecimi(link)
    scrapeProducts.setProductsDB(link)
    link = scrapeProducts.getSqliteLink()
    scrapeProducts.getProductsReview(link)


if __name__ == '__main__':
    main()
