import pandas as pd
import matplotlib.pyplot as plt

# Charger les données nettoyées
df = pd.read_csv("data/100_books_cleaned.csv")

# 1. Distribution des prix
plt.figure(figsize=(10, 6))
plt.hist(df['price'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
plt.title('Distribution des prix des livres')
plt.xlabel('Prix (£)')
plt.ylabel('Nombre de livres')
plt.grid(True, alpha=0.3)
plt.savefig('data/price_distribution.png')
plt.close()

# 2. Top 10 des livres les plus chers
top_expensive = df.sort_values('price', ascending=False).head(10)
plt.figure(figsize=(12, 8))
plt.barh(top_expensive['title'], top_expensive['price'], color='coral')
plt.title('Top 10 des livres les plus chers')
plt.xlabel('Prix (£)')
plt.tight_layout()
plt.savefig('data/top_expensive_books.png')
plt.close()

# 3. Top 10 des livres les moins chers
top_cheap = df.sort_values('price').head(10)
plt.figure(figsize=(12, 8))
plt.barh(top_cheap['title'], top_cheap['price'], color='lightgreen')
plt.title('Top 10 des livres les moins chers')
plt.xlabel('Prix (£)')
plt.tight_layout()
plt.savefig('data/top_cheap_books.png')
plt.close()

# Enregistrer quelques statistiques dans un fichier texte
with open('data/book_stats.txt', 'w') as f:
    f.write(f"Nombre total de livres: {len(df)}\n")
    f.write(f"Prix moyen: £{df['price'].mean():.2f}\n")
    f.write(f"Prix médian: £{df['price'].median():.2f}\n")
    f.write(f"Prix minimum: £{df['price'].min():.2f}\n")
    f.write(f"Prix maximum: £{df['price'].max():.2f}\n")
    f.write(f"Écart-type des prix: £{df['price'].std():.2f}\n")

print("Analyses et visualisations générées avec succès!")