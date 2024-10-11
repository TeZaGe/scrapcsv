import os 
import pandas as pd
import mysql.connector as mysql

# Récupérer le répertoire du script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Chargement des données
df = pd.read_csv("etablissements.csv", sep=",", encoding="utf-8")

# Sélection des colonnes et renommage
df = df[['denominationUniteLegale', 'denominationUsuelleEtablissement', 'dateCreationEtablissement', 'typeVoieEtablissement', 'libelleVoieEtablissement', 'libelleCommuneEtablissement', 'codePostalEtablissement', 'sexeUniteLegale', 'prenom1UniteLegale', 'nomUniteLegale']]
df.columns = ['name_entreprise', 'name_establishment', 'creation_date', 'type_way', 'address', 'city', 'postal_code', 'gender', 'first_name', 'last_name']

# Ajout des colonnes supplémentaires avec des valeurs par défaut
df['brewery_status'] = 0  # Définir `brewery_status` à 0 par défaut
df['created_by'] = None
df['last_modification_date'] = None
df['last_modified_by'] = None

# Réorganisation des colonnes, sans `brewery_id`, `mail` et `password`
df = df[['name_entreprise', 'name_establishment', 'creation_date', 'type_way', 
         'address', 'city', 'postal_code', 'gender', 'first_name', 'last_name', 
         'brewery_status', 'created_by', 'last_modification_date', 'last_modified_by']]

# Exporter le DataFrame en fichier CSV
df.to_csv("brewery.csv", index=False, encoding="utf-8")

# Connexion à la base de données
db = mysql.connect(
    host="localhost",
    user="root",
    password="",
    database="sae5",
    allow_local_infile=True
)

cursor = db.cursor()

# Retirer les colonnes inutilisées (`brewery_id`, `mail`, `password`) et insérer dans la base de données
for _, row in df.iterrows():
    sql = """
    INSERT INTO brewery (name_entreprise, name_establishment, 
                         creation_date, type_way, address, city, postal_code, gender, 
                         first_name, last_name, brewery_status, created_by, 
                         last_modification_date, last_modified_by)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # Créez le tuple de valeurs pour correspondre exactement aux colonnes SQL
    values = (row['name_entreprise'], row['name_establishment'], row['creation_date'],
              row['type_way'], row['address'], row['city'], row['postal_code'],
              row['gender'], row['first_name'], row['last_name'],
              row['brewery_status'], row['created_by'], row['last_modification_date'],
              row['last_modified_by'])
    
    try:
        cursor.execute(sql, values)
    except mysql.Error as err:
        print(f"Erreur lors de l'insertion: {err}")

# Valider les modifications
db.commit()

# Fermer le curseur et la connexion
cursor.close()
db.close()
