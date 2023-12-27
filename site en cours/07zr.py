

#################### connexion pour voir prix #################################


import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# dimension = pd.read_excel('Copie de Ranking.xlsx', sheet_name='Feuil1')
# liste_articles = dimension['Dimension'].to_list()
liste_articles = ["2055516V91"]

saisons = ["été", "4 saisons"]

marques = ["Michelin", "Continental", "Bridgestone",  'Dunlop',  'Goodyear',
           'Kleber', 'Firestone', 'Vredestein', "Hankook", 'Uniroyal', 'Kormoran', 'Tourador']


def search_article(driver, liste_article):
    search_article = driver.find_element(
        By.XPATH, '//*[@id="tab01"]/form/fieldset/div[2]/input')
    search_article.send_keys(liste_article[0:7])
    time.sleep(1)
    search_article.send_keys(Keys.ENTER)
    time.sleep(15)


def select_saison(driver, saisons):
    hiver = driver.find_element(
        By.ID, 'saison-1')
    ete = driver.find_element(
        By.ID, 'saison-2')
    tts = driver.find_element(
        By.ID, 'saison-3')
    if 'hiver' in saisons:
        hiver.click()
        time.sleep(6)
    if 'été' in saisons:
        ete.click()
        time.sleep(6)
    if '4 saisons' in saisons:
        tts.click()
        time.sleep(6)


def select_charge(driver, liste_article):
    try:
        if len(liste_article) == 10:
            driver.find_element(
                By.XPATH, f'//label[@for="charge-{liste_article[8:10]}"]').click()
            time.sleep(6)
        else:
            element = driver.find_element(
                By.XPATH, f'//label[@for="charge-{liste_article[8:11]}"]').click()
            time.sleep(6)
    except Exception as ex:
        print(ex)
        pass


def select_vitesse(driver, liste_article):
    try:
        driver.find_element(
            By.XPATH, f'//label[@for="vitesse-{liste_article[7:8].lower()}"]').click()
        time.sleep(6)
    except Exception as ex:
        print(ex)
        pass


def scrap_07zr(liste_articles, saisons, marques):

    driver = webdriver.Firefox('')
    driver.get("https://07zr.com/fr")
    time.sleep(3)

    driver.find_element(
        By.XPATH, '//*[@id="menuDesktop"]/div/ul/li[2]/a').click()

    data = []

    for liste_article in liste_articles:
        search_article(driver, liste_article)
        select_saison(driver, saisons)
        select_charge(driver, liste_article)
        select_vitesse(driver, liste_article)
        driver.find_element(By.XPATH, '//label[@for="type-14"]').click()
        time.sleep(5)


if __name__ == "__main__":
    scrap_07zr(liste_articles, saisons, marques)
