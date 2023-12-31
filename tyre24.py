import os
import re
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from dotenv import load_dotenv
from sqlalchemy import create_engine
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# lecture d'un fichier excel et mise des donées en tableau
# dimension = pd.read_excel('Copie de Ranking.xlsx', sheet_name='Feuil1')
# liste_articles = dimension['Dimension'].to_list()
liste_articles = ["2056516T107"]

saisons = ["été", "4 saisons"]

marques = ["Michelin", "Continental", "Bridgestone",  'Dunlop',  'Goodyear',
           'Kleber', 'Firestone', 'Vredestein', "Hankook", 'Uniroyal', 'Kormoran', 'Tourador']


load_dotenv()


def scroll_to_bottom(driver):
    # Exécuter du code JavaScript pour faire défiler la page jusqu'en bas
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Attendre un court moment pour que la page se charge
    time.sleep(5)


def login(driver):
    """
    fonction qui refuse les cookies et qui remplie les champs login et password et valide 

    """
    driver.find_element(
        By.XPATH, '//*[@id="alzura-cookie-consent"]/div/div/div/div[2]/a[1]').click()
    time.sleep(2)

    login = driver.find_element(By.NAME, "userid")
    login.send_keys(os.getenv('TYRE24_LOG'))
    time.sleep(1)

    password = driver.find_element(By.NAME, "password")
    password.send_keys(os.getenv('TRYE24_PASS'))
    time.sleep(1)

    password.send_keys(Keys.ENTER)
    time.sleep(10)


def cliquer_sur_pneus_charge(driver, article):
    """
    fonction qui rajout l'indice de charge pour la recherche

    """
    if article == 10:
        xpath_saison = f'//span[contains(text(), "{article[8:10]}")]'
    else:
        xpath_saison = f'//span[contains(text(), "{article[8:11]}")]'

    try:
        element = driver.find_element(By.XPATH, xpath_saison)
        # Faire défiler jusqu'à l'élément pour le rendre visible
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        time.sleep(3)
    except:
        pass


def cliquer_sur_pneus_selon_saison(driver, saison_texte):
    """
    fonction qui sert a selectionné les champs de saison
    """
    xpath_saison = f'//span[contains(text(), "Pneus {saison_texte}")]'

    try:
        element = driver.find_element(By.XPATH, xpath_saison)
        # Faire défiler jusqu'à l'élément pour le rendre visible
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        time.sleep(3)
    except:
        pass


def select_saisons(driver, saisons):
    """
    fonction qui valide les champs de saison selon les saison du tableau saison
    """
    if "été" in saisons:
        cliquer_sur_pneus_selon_saison(driver, "été")

    if "hiver" in saisons:
        cliquer_sur_pneus_selon_saison(driver, "hiver")

    if "4 saisons" in saisons:
        cliquer_sur_pneus_selon_saison(driver, "4 saisons")
        time.sleep(5)


def extract_article_info(article, driver, liste_article):
    """
    fonction qui extrait les info de chaque article et les retourne sous forme de dictionnaire
    """
    try:
        profil = article.find_element(
            By.XPATH, "div[4]/div[2]/p[2]")

        profil_no_M = profil.text.split(' ', 1)
        pattern = re.compile(
            f"{re.escape(liste_article[0:3])}(.*?){re.escape(liste_article[7:8])}", re.DOTALL)
        resultat = pattern.search(profil.text)
        texte_extrait = resultat.group(1).replace(
            '/', '').replace(' ', '')
        dim_L = profil_no_M[1]
        dim = dim_L.split(' ', 1)
        dim_T = dim[1]
        date_du_jour = datetime.now().strftime("%d-%m-%Y")
        complement = article.find_element(
            By.XPATH, 'div[4]/div[2]/p[1]')
        prix = article.find_element(
            By.XPATH, 'div[5]/div[2]/div/div/span')
        saison = article.find_element(
            By.XPATH, 'div[4]/div[2]/div')
        saison_clean = saison.text.split(' ', 1)
        indice = profil_no_M[1]

        if len(liste_article) == 10:
            code = dim_T[0:3] + texte_extrait[0:5].replace(
                'R', '') + indice[-1] + texte_extrait[5:7]
            code_article = dim_T[0:3] + texte_extrait[0:5] + indice[-1] + texte_extrait[5:7] + \
                complement.text.replace(' ', '').replace('.', '')
        else:
            code = dim_T[0:3] + texte_extrait[0:5].replace(
                'R', '') + indice[-1] + texte_extrait[5:8]
            code_article = dim_T[0:3] + texte_extrait[0:5] + indice[-1] + texte_extrait[5:8] + \
                complement.text.replace(' ', '').replace('.', '')
        article_info = {

            'Code': code,
            'Marque': profil_no_M[0].capitalize(),
            'Code article': code_article.upper(),
            'Prix': prix.text.replace('€', '').replace(',', '.'),
            'Saison': saison_clean[1],
            'Date': date_du_jour,
            'Site': 'Tyre24'
        }

        if liste_article != article_info["Code"]:
            return None
        else:
            print(article_info)
            return article_info
    except Exception as ex:
        print(ex)
        return None


def save_donnees_sql(data, marques):
    """
    fonction de sauvegarde des données en SQL
    """

    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    ID = os.getenv('ID')
    DATABASE = os.getenv('DATABASE')
    PASSWORD = os.getenv('PASSWORD')

    connection_string = f"postgresql+psycopg2://{ID}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    engine = create_engine(connection_string)

    data = [item for item in data if item is not None]

    df = pd.DataFrame(data)
    df.replace('été', 'Eté', inplace=True)

    data_final = pd.DataFrame()

    for i in marques:
        data_clean = df[df['Marque'] == i]
        data_final = pd.concat([data_final, data_clean])

    data_final.to_sql('scrap_pneu', engine, if_exists='append', index=False)


def scrap_tyre24(liste_articles, saisons, marques):
    """
    fonction principal pour le scrap
    """

    driver = webdriver.Firefox('')
    driver.get(
        "https://tyre24.alzura.com/fr/fr")
    time.sleep(2)

    login(driver)

    data = []

    for liste_article in liste_articles:
        driver.find_element(
            By.XPATH, '//*[@id="megaMenu"]/ul/li[1]/a').click()
        time.sleep(5)
        search_article = driver.find_element(
            By.XPATH, '//*[@id="vs1__combobox"]/div[1]/input')
        search_article.send_keys(f"{liste_article[0:8]}")
        time.sleep(1)
        search_article.send_keys(Keys.ENTER)
        time.sleep(7)
        cliquer_sur_pneus_charge(driver, liste_article)
        select_saisons(driver, saisons)
        for i in range(0, 100):
            try:
                scroll_to_bottom(driver)
                page = driver.find_element(
                    By.XPATH, f'//*[@id="rdxpg_{i}"]/span')
            except:
                break

        articles = driver.find_elements(
            By.CLASS_NAME, 'item')

        for article in articles:
            article_info = extract_article_info(article, driver, liste_article)
            data.append(article_info)

    save_donnees_sql(data, marques)

    driver.quit()


if __name__ == "__main__":
    scrap_tyre24(liste_articles, saisons, marques)
