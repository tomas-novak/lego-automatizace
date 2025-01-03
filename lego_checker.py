import csv
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# URL produktů
URLS = [
    "https://www.lego.com/cs-cz/product/legolas-gimli-40751",
    "https://www.lego.com/cs-cz/product/tudor-corner-10350"
]

# Funkce pro kontrolu dostupnosti a ceny
def fetch_data():
    results = []
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Režim bez okna
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")  # Potlačí většinu výstupů Chromu
    options.add_argument("--disable-logging")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    for url in URLS:
        print(f"Zpracovávám URL: {url}")
        driver.get(url)

        # Extrakce dostupnosti
        try:
            availability_element = driver.find_element(By.CSS_SELECTOR, '[data-test="product-overview-availability"]')
            availability = availability_element.text
        except Exception:
            availability = "Dostupnost nenalezena"

        # Extrakce ceny
        try:
            price_element = driver.find_element(By.CSS_SELECTOR, '[data-test="product-price"]')
            price = price_element.text
        except Exception:
            price = "Cena nenalezena"

        # Přidání výsledků do seznamu
        results.append([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            url,
            availability,
            price
        ])

    driver.quit()
    return results

# Funkce pro přidání dat do CSV
def append_to_csv(file_name, data):
    file_exists = os.path.isfile(file_name)

    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Přidejte záhlaví, pokud soubor ještě neexistuje
        if not file_exists:
            writer.writerow(["timestamp", "set_url", "availability", "price"])

        # Přidejte nové řádky
        writer.writerows(data)

# Použití funkcí
file_name = "lego_results.csv"
data = fetch_data()
append_to_csv(file_name, data)