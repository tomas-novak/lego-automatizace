import csv
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Konfigurace SMTP pro Seznam.cz
SMTP_SERVER = "smtp.seznam.cz"
SMTP_PORT = 587
EMAIL_ADDRESS = "your-email@seznam.cz"  # Váš e-mail
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Heslo načtené z GitHub Secrets

# URL produktů
URLS = [
    "https://www.lego.com/cs-cz/product/legolas-gimli-40751",
    "https://www.lego.com/cs-cz/product/tudor-corner-10350"
]

# Funkce pro kontrolu dostupnosti a ceny
def fetch_data():
    results = []
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
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
        if isinstance(results, list):
            results.append([
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                url,
                availability,
                price
            ])
        else:
            print("Chyba: Results musí být seznam.")

    driver.quit()
    return results

# Funkce pro načtení předchozích dat
def load_previous_data(file_name):
    if not os.path.isfile(file_name):
        return {}
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Přeskočte záhlaví
        return {row[1]: (row[2], row[3]) for row in reader}

# Funkce pro odesílání e-mailu
def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        print("E-mail byl úspěšně odeslán.")

# Funkce pro porovnání a detekci změn
def check_for_changes(previous_data, current_data):
    changes = []
    for timestamp, url, availability, price in current_data:
        if url not in previous_data:
            changes.append(f"Nový záznam pro {url}:
 - Dostupnost: {availability}
 - Cena: {price}")
        else:
            prev_availability, prev_price = previous_data[url]
            if availability != prev_availability or price != prev_price:
                changes.append(f"Změna pro {url}:
 - Dostupnost: {prev_availability} -> {availability}
 - Cena: {prev_price} -> {price}")
    return changes

# Funkce pro uložení aktuálních dat
def save_data(file_name, data):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "url", "availability", "price"])
        if isinstance(data, list) and all(isinstance(row, list) for row in data):
            writer.writerows(data)
        else:
            print("Chyba: Data musí být seznam obsahující seznamy.")

# Hlavní část skriptu
file_name = "lego_results.csv"
previous_data = load_previous_data(file_name)
current_data = fetch_data()
changes = check_for_changes(previous_data, current_data)

if changes:
    change_message = "\n\n".join(changes)
    send_email("Změny na LEGO stránkách", change_message)

save_data(file_name, current_data)