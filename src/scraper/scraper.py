# scraper.py (version corrigée avec limite de 100 livres)
import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import random
from urllib.parse import urljoin
from typing import List, Tuple
from config import BASE_URL, HEADERS, DELAY

# Nouvelle variable globale pour le compteur
TOTAL_BOOKS_LIMIT = 100
total_books_scraped = 0

def get_all_categories() -> List[Tuple[str, str]]:
    """
    Récupère toutes les catégories de livres sous forme de liste de tuples (nom, URL).
    """
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des catégories : {e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    category_links = soup.select("ul.nav-list li a")
    
    categories = []
    for link in category_links:
        name = link.text.strip()
        url = urljoin(BASE_URL, link["href"])
        categories.append((name, url))
    
    return categories

def scrape_single_page(page_url: str) -> List[dict]:
    """
    Scrape une seule page de livres et retourne une liste de dictionnaires contenant les données.
    """
    global total_books_scraped
    
    try:
        response = requests.get(page_url, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur avec {page_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    data = []
    for book in books:
        if total_books_scraped >= TOTAL_BOOKS_LIMIT:
            break
            
        try:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            relative_link = book.h3.a["href"]
            full_link = urljoin(page_url, relative_link)
            
            data.append({
                "title": title,
                "price": price,
                "link": full_link
            })
            total_books_scraped += 1
        except Exception as e:
            print(f"Erreur lors du scraping d'un livre: {e}")
    
    return data

def scrape_all_pages(category_url: str) -> List[dict]:
    """
    Scrape toutes les pages d'une catégorie jusqu'à atteindre la limite de TOTAL_BOOKS_LIMIT.
    """
    global total_books_scraped
    
    all_books = []
    while True:
        if total_books_scraped >= TOTAL_BOOKS_LIMIT:
            break
            
        print(f"Scraping {category_url}")
        books = scrape_single_page(category_url)
        all_books.extend(books)
        
        if total_books_scraped >= TOTAL_BOOKS_LIMIT:
            break
        
        # Vérifier s'il y a une page suivante
        try:
            soup = BeautifulSoup(requests.get(category_url, headers=HEADERS).text, "html.parser")
            next_button = soup.find("li", class_="next")
            
            if not next_button:
                break
                
            next_page = next_button.a["href"]
            category_url = urljoin(category_url, next_page)
            time.sleep(DELAY + random.uniform(0, 1))
        except Exception as e:
            print(f"Erreur lors de la pagination: {e}")
            break
    
    return all_books

def save_to_csv(data: List[dict], filename: str):
    """
    Enregistre les données scrapées dans un fichier CSV.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "price", "link"])
        writer.writeheader()
        writer.writerows(data)

def main():
    global total_books_scraped
    
    categories = get_all_categories()
    if not categories:
        print("Aucune catégorie trouvée")
        return
    
    all_books = []
    for cat_name, cat_url in categories:
        if total_books_scraped >= TOTAL_BOOKS_LIMIT:
            break
            
        print(f"\nScraping de la catégorie : {cat_name}")
        books = scrape_all_pages(cat_url)
        all_books.extend(books)
        time.sleep(DELAY * 2)
    
    save_to_csv(all_books, "data/100_books.csv")
    print(f"\n{len(all_books)} livres scrapés (limite de {TOTAL_BOOKS_LIMIT} atteinte) !")

if __name__ == "__main__":
    main()
