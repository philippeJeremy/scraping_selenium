import time
import os
import smtplib
from dotenv import load_dotenv
from gettygo import gettygo_scrap
from tyre24 import scrap_tyre24
from centralepneus import scrap_centralepneus
from email.mime.text import MIMEText
from carleader import carleader_scrap
from districash import districash_scrap
from email.mime.multipart import MIMEMultipart

# dimension = pd.read_excel('Copie de Ranking.xlsx', sheet_name='Feuil1')
# liste_articles = dimension['Dimension'].to_list()

load_dotenv()

liste_articles = ["2055516V91"]

saisons_disti = ["été", "hiver", "4 saisons"]
saisons = ["été", "4 saisons"]
marques = ["Michelin", "Continental", "Bridgestone",  'Dunlop',  'Goodyear',
           'Kleber', 'Firestone', 'Vredestein', "Hankook", 'Uniroyal', 'Kormoran', 'Tourador']

# mail si erreur lors de l'éxecution


def send_email(subject, content):
    sender_email = os.getenv("SENDMAIL")
    sender_password = os.getenv("PWDMAIL")
    receiver_email = os.getenv("RECMAIL")

    # Créez le message
    message = MIMEMultipart()
    message.attach(MIMEText(content, 'plain'))
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email

    # Établissez une connexion SMTP sécurisée
    with smtplib.SMTP_SSL("smtp.laposte.net", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())


try:
    carleader_scrap(liste_articles, saisons, marques)
    time.sleep(20)
except Exception as ex:
    error_message = str(ex)
    print(error_message)
    send_email("Erreur scrap web", error_message)
try:
    districash_scrap(liste_articles, saisons_disti)
    time.sleep(20)
except Exception as ex:
    error_message = str(ex)
    print(error_message)
    send_email("Erreur scrap web", error_message)
try:
    gettygo_scrap(liste_articles, saisons, marques)
    time.sleep(20)
except Exception as ex:
    error_message = str(ex)
    print(error_message)
    send_email("Erreur scrap web", error_message)
try:
    scrap_tyre24(liste_articles, saisons, marques)
    time.sleep(20)
except Exception as ex:
    error_message = str(ex)
    print(error_message)
    send_email("Erreur scrap web", error_message)
try:
    scrap_centralepneus(liste_articles, saisons, marques)
    time.sleep(20)
except Exception as ex:
    error_message = str(ex)
    print(error_message)
    send_email("Erreur scrap web", error_message)
