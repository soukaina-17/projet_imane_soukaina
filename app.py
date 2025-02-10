from flask import Flask, request, jsonify, redirect, render_template
from sqlalchemy import create_engine
from datetime import datetime

db_path = 'sqlite:///bdd_recette.db'

engine = create_engine(db_path)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle de recette
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Recipe {self.name}>'

# Route pour afficher et ajouter des recettes
@app.route('/recipe', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_recipe = Recipe(name=name, description=description)
        try:
            db.session.add(new_recipe)
            db.session.commit()
            return redirect('/recipe')  # Rediriger vers la page de recette
        except Exception:
            return "Une erreur s'est produite"
    else:
        recipes = Recipe.query.order_by(Recipe.created_at)
        return render_template('index.html', recipes=recipes)

# Route pour supprimer une recette
@app.route('/recipe/delete/<int:id>')
def delete(id):
    recipe_to_delete = Recipe.query.get_or_404(id)
    try:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return redirect('/recipe')  # Rediriger vers la page de recette
    except Exception:
        return "Une erreur s'est produite"

# Route pour mettre à jour une recette
@app.route('/recipe/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == 'POST':
        recipe.name = request.form['name']
        recipe.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/recipe')  # Rediriger vers la page de recette
        except Exception:
            return "Une erreur s'est produite"
    else:
        return render_template('update.html', recipe=recipe)


# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)
