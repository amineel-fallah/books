import pandas as pd

# Charger le fichier CSV
df = pd.read_csv("data/100_books.csv")
print(f"Données chargées: {df.shape[0]} livres")

# Afficher les premières lignes et les types de données
print("\nAperçu des données originales:")
print(df.head())
print("\nTypes de données:")
print(df.dtypes)

# Vérifier s'il y a des valeurs manquantes
print(f"\nValeurs manquantes: {df.isnull().sum().sum()}")

# Nettoyer la colonne des prix
if 'price' in df.columns:
    # Vérifier si la colonne est de type object (string)
    if df["price"].dtype == 'object':
        # Convertir les prix: supprimer "£" et convertir en float
        # Utiliser regex=True pour gérer les caractères spéciaux correctement
        df["price"] = df["price"].str.replace("£", "", regex=True)
        # Gérer le cas de 'Â' qui apparaît parfois devant le symbole £
        df["price"] = df["price"].str.replace("Â", "", regex=True)
        # Convertir en float
        df["price"] = pd.to_numeric(df["price"], errors='coerce')
        print("\nPrix nettoyés")

# Supprimer les doublons
duplicates_count = df.duplicated().sum()
df.drop_duplicates(inplace=True)
print(f"\n{duplicates_count} doublons supprimés")

# Supprimer les valeurs manquantes
null_count = df.isnull().sum().sum()
df.dropna(inplace=True)
print(f"{null_count} valeurs manquantes supprimées")

# Vérifier et corriger les liens
if 'link' in df.columns:
    # Compter combien de liens doivent être corrigés
    links_to_fix = df["link"].str.startswith("http").value_counts().get(False, 0)
    
    # Corriger les liens qui ne commencent pas par "http"
    df["link"] = df["link"].apply(lambda x: x if str(x).startswith("http") else "https://books.toscrape.com" + str(x))
    print(f"\n{links_to_fix} liens corrigés")

# Trier les données par prix
df = df.sort_values(by="price", ascending=True)

# Afficher quelques statistiques
print("\nStatistiques des prix après nettoyage:")
print(df["price"].describe())

# Sauvegarder les données nettoyées
df.to_csv("data/100_books_cleaned.csv", index=False)
print("\nNettoyage terminé ! Fichier enregistré sous 'data/100_books_cleaned.csv'.")