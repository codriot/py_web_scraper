# Python WebScraper

This project is a web scraper that collects product and review data from n11.com and stores it in a SQLite database.

## Installation

Clone the repository:

```bash
git clone https://github.com/codriot/py_final_project-main.git
```
Install the required Python packages:
pip install -r requirements.txt

Usage
The project contains several Python scripts that perform different tasks:

db_operations.py: Contains functions for interacting with the SQLite database. It includes functions for saving product data to the database and retrieving it with different sorting options.

products.py: Contains the allProduct function that scrapes product data from a given URL.

reviews.py: Contains the scrapeProductReview function that scrapes review data for a specific product.

To run the project, execute the main script: 

python main.py

The data in the database is saved as follows:
![image](https://github.com/codriot/py_final_project-main/assets/146637002/7416bc48-5ef1-4050-ad2e-fb3ed8d8d84b)



Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


> [!hint]
>To find the highest reviewed product, you need to press and enter 1 when prompted for category and brand, and select the one based on the number of reviews as the sort type and press 1, to find the product with both the most reviews and the highest star rate, you need to select the smart sort and enter 1 again. 


License
[MIT](https://choosealicense.com/licenses/mit/)
