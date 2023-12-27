import os
import time
import pandas as pd
import psycopg2
from datetime import datetime
from selenium import webdriver
from dotenv import load_dotenv
from openpyxl import load_workbook
from sqlalchemy import create_engine
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


dimension = pd.read_excel('Copie de Ranking.xlsx', sheet_name='Feuil1')
liste_articles = dimension['Dimension'].to_list()
# liste_articles = ['2055516V91']

saisons = ["été", "4 saisons"]

marques = ["Michelin", "Continental", "Bridgestone",  'Dunlop',  'Goodyear',
           'Kleber', 'Firestone', 'Vredestein', "Hankook", 'Uniroyal', 'Kormoran', 'Tourador']


def save_donnees_sql(data):
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    ID = os.getenv('ID')
    DATABASE = os.getenv('DATABASE')
    PASSWORD = os.getenv('PASSWORD')

    connection_string = f"postgresql+psycopg2://{ID}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    engine = create_engine(connection_string)

    data = [item for item in data if item is not None]

    df = pd.DataFrame(data)
    df.replace("", pd.NA, inplace=True)
    df.dropna(inplace=True)

    df.to_sql('scrap_pneu', engine, if_exists='append', index=False)


def select_marque(driver, marques):
    driver.find_element(
        By.XPATH, '//*[@id="home-selector"]/form/div[2]/div[8]/div[1]').click()
    time.sleep(2)

    for i in marques:
        try:
            driver.find_element(By.XPATH, f'//label[text()="{i}"]').click()
            time.sleep(2)
        except Exception as ex:
            print(ex)
            pass

    driver.find_element(
        By.XPATH, '//*[@id="selector-marque"]/div[4]/span').click()
    time.sleep(2)


def search_article(driver, liste_article):
    largeur = Select(driver.find_element(By.XPATH, '//select[@name="l"]'))
    largeur.select_by_value(f'{liste_article[0:3]}')
    time.sleep(2)
    hauteur = Select(driver.find_element(By.XPATH, '//select[@name="h"]'))
    hauteur.select_by_value(f'{liste_article[3:5]}')
    time.sleep(2)
    diametre = Select(driver.find_element(By.XPATH, '//select[@name="d"]'))
    diametre.select_by_value(f'{liste_article[5:7]}')
    time.sleep(2)
    driver.find_element(
        By.CLASS_NAME, 'upper.btn.btn-danger.btn-block.btn-large').click()
    time.sleep(5)
    if len(liste_article) == 10:
        charge = Select(driver.find_element(By.XPATH, '//select[@name="c"]'))
        charge.select_by_value(f'{liste_article[8:10]}')
        time.sleep(2)
    else:
        charge = Select(driver.find_element(By.XPATH, '//select[@name="c"]'))
        charge.select_by_value(f'{liste_article[8:11]}')
        time.sleep(2)
    vitesse = Select(driver.find_element(By.XPATH, '//select[@name="v"]'))
    vitesse.select_by_value(f'{liste_article[7:8]}')
    time.sleep(2)
    driver.find_element(
        By.CLASS_NAME, 'upper.btn.btn-danger.btn-block.btn-large').click()


def extract_article(driver, artilce, liste_article):
    date_du_jour = datetime.now().strftime("%d-%m-%Y")
    code = artilce.find_element(By.XPATH, 'td[3]/a/small')
    clean_code = code.text.split('\n')
    split_code = clean_code[0].split(' ')
    digits = ""
    letters = ""

    for char in split_code[2]:
        if char.isdigit():
            digits += char
        elif char.isalpha():
            letters += char

    code_clean = split_code[0].replace('/', '') + split_code[1].replace(
        'R', '') + letters + digits

    marque = artilce.find_element(By.XPATH, 'td[3]/a/span[1]')
    designation = artilce.find_element(By.XPATH, 'td[3]/a/span[2]')
    prix = artilce.find_element(By.XPATH, 'td[6]/div/span[1]')
    saison = artilce.find_element(By.XPATH, 'td[5]')

    article_info = {
        'Code': code_clean,
        'Marque': marque.text,
        'Code article': clean_code[0].replace('/', '').replace(' ', '') + designation.text.replace(' ', ''),
        'Designation': clean_code[0] + ' ' + marque.text + ' ' + designation.text,
        'Prix': prix.text.replace(',', '.').replace('€', ''),
        'Saison': saison.text.replace('Tourisme ', ''),
        'Date': date_du_jour,
        'Site': 'Centralepneus'
    }

    if liste_article != article_info["Code"]:
        return None
    else:
        print(article_info)
        return article_info


def scrap_centralepneus(liste_articles, saisons, marques):

    # connexion au site web
    driver = webdriver.Firefox('')
    driver.get("https://www.centralepneus.fr/")
    time.sleep(2)

    data = []

    driver.find_element(By.XPATH, '/html/body/div[8]/div[1]/a').click()
    time.sleep(2)

    select_marque(driver, marques)

    for liste_article in liste_articles:
        search_article(driver, liste_article)
        articles = driver.find_elements(By.CLASS_NAME, 'tr-to-product')
        for artilce in articles:
            article_info = extract_article(driver, artilce, liste_article)
            data.append(article_info)

    save_donnees_sql(data)

    driver.quit()


if __name__ == "__main__":
    scrap_centralepneus(liste_articles, saisons, marques)
