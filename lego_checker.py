from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# URL produktů
URLS = [
    "https://www.lego.com/cs-cz/product/legolas-gimli-40751",
    "https://www.lego.com/cs-cz/product/tudor-corner-10350"
]

# Funkce pro kontrolu dostupnosti
def check_availability():
    try:
        # Nastavení pro WebDriver s použitím WebDriver Manager
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Režim bez okna
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")  # Potlačí většinu výstupů Chromu
        options.add_argument("--disable-logging")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        for url in URLS:
            print(f"Kontroluji dostupnost na URL: {url}")
            driver.get(url)
            time.sleep(5)  # Počkejte na načtení obsahu stránky

            # Najdi element s informací o dostupnosti
            try:
                availability_element = driver.find_element(By.CSS_SELECTOR, '[data-test="product-overview-availability"]')
                print(f"Stav na stránkách LEGO ({url}): {availability_element.text}")
            except Exception:
                print(f"Nepodařilo se najít informace o dostupnosti na stránkách ({url}).")

        driver.quit()
    except Exception as e:
        print(f"Došlo k chybě při kontrole dostupnosti: {e}")

# Spuštění kontroly
if __name__ == "__main__":
    check_availability()
