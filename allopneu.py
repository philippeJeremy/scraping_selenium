
##################### anti-bot corriace ################

import time
import pandas as pd
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# dimension = pd.read_excel('Copie de Ranking.xlsx', sheet_name='Feuil1')
# liste_articles = dimension['Dimension'].to_list()
liste_articles = ['2055516V91']

saisons = ["été", "4 saisons"]

marques = ["Michelin", "Continental", "Bridgestone",  'Dunlop',  'Goodyear',
           'Kleber', 'Firestone', 'Vredestein', "Hankook", 'Uniroyal', 'Kormoran', 'Tourador']

load_dotenv()


def pass_anti_bot(driver):
    driver.find_element(By.ID, 'L2AGLb').click()
    input_recherche = driver.find_element(By.ID, 'APjFqb')
    input_recherche.send_keys("allopneu")
    time.sleep(1)
    input_recherche.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element(
        By.CSS_SELECTOR, 'a[href="https://www.allopneus.com/"]').click()
    time.sleep(3)
    driver.find_element(
        By.CLASS_NAME, 'onetrust-close-btn-handler.banner-close-button.ot-close-link').click()


def select_saison(driver, saisons):
    saison_ete = driver.find_element(By.ID, "ete")
    if 'été' in saisons:
        if saison_ete.is_selected():
            pass
        else:
            driver.execute_script("arguments[0].click();", saison_ete)
            time.sleep(2)
    else:
        if saison_ete.is_selected():
            driver.execute_script("arguments[0].click();", saison_ete)
            time.sleep(2)
    saison_4saison = driver.find_element(By.ID, "4seasons")
    if '4 saisons' in saisons:
        if saison_4saison.is_selected():
            pass
        else:
            driver.execute_script(
                "arguments[0].click();", saison_4saison)
            time.sleep(2)
    else:
        if saison_4saison.is_selected():
            driver.execute_script(
                "arguments[0].click();", saison_4saison)
            time.sleep(2)
    saison_hiver = driver.find_element(By.ID, "hiver")
    if 'hiver' in saisons:
        if saison_hiver.is_selected():
            pass
        else:
            driver.execute_script(
                "arguments[0].click();", saison_hiver)
            time.sleep(2)
    else:
        if saison_hiver.is_selected():
            driver.execute_script(
                "arguments[0].click();", saison_hiver)
            time.sleep(2)


def select_charge_vitesse(driver, liste_article):
    try:
        driver.find_element(By.ID, 'tire_search_load').click()
        time.sleep(4)
        if len(liste_article) == 10:
            driver.find_element(
                By.XPATH, f'//label[@for="load_{liste_article[8:10]}"]').click()
            time.sleep(4)
        else:
            driver.find_element(
                By.XPATH, f'//label[@for="load_{liste_article[8:11]}"]').click()
            time.sleep(4)
        driver.find_element(
            By.XPATH, f'//label[@for="speed_{liste_article[7:8]}"]').click()
        time.sleep(4)
        driver.find_element(
            By.XPATH, '//*[@id="app_product_search_form_by_dimension_root"]/div[3]/div/div[5]/button').click()
        time.sleep(5)

    except Exception as ex:
        print(ex)
        pass


def gettygo_scrap(liste_articles, saisons, marques):
    driver = webdriver.Firefox('')

    driver.get(
        "https://google.com")

    time.sleep(2)

    data = []

    pass_anti_bot(driver)

    for liste_article in liste_articles:
        try:
            time.sleep(3)
            driver.find_element(
                By.CLASS_NAME, 'textual-search__icon').click()
            time.sleep(3)
            search = driver.find_element(
                By.ID, 'textual-search-input')
            search.send_keys(liste_article[0:7])
            time.sleep(3)
            search.send_keys(Keys.ENTER)
            time.sleep(3)
            select_saison(driver, saisons)
            select_charge_vitesse(driver, liste_article)
            driver.find_element(
                By.XPATH, '//*[@id="accordion__panel-brand"]/button').click()
            time.sleep(2)

            for i in marques:
                print(i)
                try:
                    driver.find_element(
                        By.ID, f'//label[@for="{i.lower()}"]').click()
                    time.sleep(3)
                except:
                    pass

            articles = driver.find_elements(By.CLASS_NAME, 'listing-row')

            # for article in articles:
            #     pass

            # try:
            #     while True:
            #         driver.find_element(
            #             By.XPATH, '//*[@id="js-listing-container"]/ul/li[8]/a').click()
            #         time.sleep(5)
            #         articles = driver.find_elements(
            #             By.CLASS_NAME, 'listing-row')
            #         for article in articles:
            #             pass
            # except:
            #     pass

        except Exception as ex:
            print('pas bon')
            print(ex)

        for article in articles:
            try:
                marque = article.find_elements()

                #     article_info = {
                #     'Marque': marque.text,
                #     # 'Code': code.text,
                #     'Designation': designation.text,
                #     'Prix': prix.text,
                #     'Saison': saison
                # }
                # data.append(article_info)
            except Exception as ex:
                print(ex)


if __name__ == "__main__":
    gettygo_scrap(liste_articles, saisons, marques)
