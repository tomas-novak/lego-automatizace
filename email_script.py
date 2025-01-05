import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Konfigurace SMTP pro Seznam.cz
SMTP_SERVER = "smtp.seznam.cz"
SMTP_PORT = 465
EMAIL_ADDRESS = "novaktomas111@seznam.cz"  # Váš e-mail
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Heslo načtené z proměnné prostředí

def send_test_email():
    subject = "Testovací e-mail"
    body = "Toto je jednoduchý testovací e-mail odeslaný skriptem."

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "novaktomas111@gmail.com"
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Použití SSL připojení
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, "novaktomas111@gmail.com", msg.as_string())
            print("Testovací e-mail byl úspěšně odeslán.")
    except Exception as e:
        print(f"Chyba při odesílání e-mailu: {e}")

# Spuštění testovací funkce
if __name__ == "__main__":
    if EMAIL_PASSWORD is None:
        print("Chyba: Heslo nebylo nalezeno. Zkontrolujte, zda je proměnná EMAIL_PASSWORD nastavena v systému.")
    else:
        send_test_email()