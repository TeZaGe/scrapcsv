from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import os
import time
import glob
import mysql.connector as mysql

# Récupérer le répertoire du script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Supprimer les fichiers CSV existants dans le répértoire
csv_files = glob.glob(os.path.join(script_dir, "*.csv"))
for file in csv_files:
    try:
        os.remove(file)
        print(f"Supprimé : {file}")
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier {file}: {e}")


# Configurer les options du navigateur
chrome_options = Options()
chrome_options.add_experimental_option("detach", True) 

# Configurer le répertoire de téléchargement
prefs = {
    "download.default_directory": script_dir,  # Répertoire de téléchargement
    "download.prompt_for_download": False,     # Ne pas demander où télécharger
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

service = Service('./chromedriver.exe')

driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://sirene.fr/sirene/public/creation-fichier#activite-principale")

    
    time.sleep(2) 

    # Trouver le menu déroulant
    select_element = driver.find_element(By.ID, "preselect-activite-sousClasse")
    select = Select(select_element)

    # valeur 11 = fabrication de boissons
    select.select_by_value('11')

    
    time.sleep(1) 

    #valeur 1105Z = fabrication de bière
    driver.find_element(By.ID, "1105Z-selectable").click()

    
    time.sleep(1)  

    driver.find_element(By.ID, "button-submit").click()

    
    time.sleep(5)

   
    calculer_btn = driver.find_element(By.ID, "lien-obtenir-devis")
    
    
    driver.execute_script("arguments[0].click();", calculer_btn)

   
    time.sleep(5)

   
    driver.find_element(By.ID, "button-etape-3").click()

    
    time.sleep(10)  

finally:
    
    driver.quit()



# Chargement des données
df = pd.read_csv("etablissements.csv", sep=",", encoding="utf-8")

# Sélection des colonnes et renommage
df = df[['denominationUniteLegale', 'denominationUsuelleEtablissement', 'dateCreationEtablissement', 'typeVoieEtablissement', 'libelleVoieEtablissement', 'libelleCommuneEtablissement', 'codePostalEtablissement', 'sexeUniteLegale', 'prenom1UniteLegale', 'nomUniteLegale']]
df.columns = ['name_entreprise', 'name_establishment', 'creation_date', 'type_way', 'address', 'city', 'postal_code', 'gender', 'first_name', 'last_name']

# Ajout des colonnes supplémentaires
df['brewery_id'] = None
df['mail'] = None
df['password'] = None
df['brewery_status'] = None
df['created_by'] = None
df['last_modification_date'] = None
df['last_modified_by'] = None

# Réorganisation des colonnes
df = df[['brewery_id', 'mail', 'password', 'name_entreprise', 'name_establishment', 'creation_date', 'type_way', 'address', 'city', 'postal_code', 'gender', 'first_name', 'last_name', 'brewery_status', 'created_by', 'last_modification_date', 'last_modified_by']]

# Exporter le DataFrame en fichier CSV
df.to_csv("brewery.csv", index=False, encoding="utf-8")




