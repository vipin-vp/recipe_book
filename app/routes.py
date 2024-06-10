# app/routes.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import app, db
from .models import User, Recipe


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/recipes', methods=['GET'])
@login_required
def recipes():
    page = request.args.get('page', 1, type=int)
    results = Recipe.query.filter_by(created_by=current_user.id).paginate(page=page, per_page=10)
    return render_template('recipes.html', recipes=results)


@app.route('/recipes/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        new_recipe = Recipe(title=title, description=description, ingredients=ingredients, instructions=instructions, created_by=current_user.id)
        db.session.add(new_recipe)
        db.session.commit()
        flash('Recipe added successfully', 'success')
        return redirect(url_for('recipes'))
    return render_template('add_recipe.html')


@app.route('/recipes/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', recipe=recipe)


@app.route('/recipes/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.method == 'POST':
        recipe.title = request.form.get('title')
        recipe.description = request.form.get('description')
        recipe.ingredients = request.form.get('ingredients')
        recipe.instructions = request.form.get('instructions')
        db.session.commit()
        flash('Recipe updated successfully', 'success')
        return redirect(url_for('recipes'))
    return render_template('edit_recipe.html', recipe=recipe)


@app.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully', 'success')
    return redirect(url_for('recipes'))


@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')
    results = Recipe.query.filter(Recipe.title.ilike(f'%{query}%') | Recipe.ingredients.ilike(f'%{query}%')).all()
    return render_template('search_results.html', recipes=results)
