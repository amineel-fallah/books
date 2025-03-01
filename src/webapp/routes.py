from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html', title='Accueil')

@main_bp.route('/books')
def books():
    """Page affichant tous les livres"""
    # Charger les données des livres
    csv_path = os.path.join('data', '100_books.csv')
    
    if not os.path.exists(csv_path):
        return render_template('books.html', 
                              title='Livres', 
                              books=[], 
                              error="Fichier de données non trouvé")
    
    books_df = pd.read_csv(csv_path)
    books_list = books_df.to_dict('records')
    
    # Obtenir les filtres de l'URL (si présents)
    price_filter = request.args.get('price')
    if price_filter:
        # Nettoyer la valeur du prix et filtrer les livres
        try:
            price_filter = float(price_filter.replace('£', '').strip())
            books_list = [book for book in books_list 
                         if float(book['price'].replace('£', '').strip()) <= price_filter]
        except ValueError:
            pass
    
    return render_template('books.html', 
                          title='Livres', 
                          books=books_list,
                          count=len(books_list))

@main_bp.route('/api/books')
def api_books():
    """API pour obtenir les données des livres au format JSON"""
    csv_path = os.path.join('data', '100_books.csv')
    
    if not os.path.exists(csv_path):
        return jsonify({"error": "Data file not found"}), 404
    
    books_df = pd.read_csv(csv_path)
    books_list = books_df.to_dict('records')
    
    return jsonify(books_list)