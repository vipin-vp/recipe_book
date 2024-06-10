# tests/test_recipe.py

import pytest
from app import db
from app.models import Recipe
from test_conftest import client, login


def test_add_recipe(client, login):
    login()
    response = client.post('/recipes/add', data={
        'title': 'Test Recipe',
        'description': 'Test Description',
        'ingredients': 'Test Ingredients',
        'instructions': 'Test Instructions'
    })
    assert response.status_code == 302  # Redirect to recipes page
    recipe = Recipe.query.filter_by(title='Test Recipe').first()
    assert recipe is not None


def test_edit_recipe(client, login):
    login()
    recipe = Recipe(title='Test Recipe', description='Test Description', ingredients='Test Ingredients', instructions='Test Instructions', created_by=1)
    db.session.add(recipe)
    db.session.commit()

    response = client.post(f'/recipes/{recipe.id}/edit', data={
        'title': 'Updated Recipe',
        'description': 'Updated Description',
        'ingredients': 'Updated Ingredients',
        'instructions': 'Updated Instructions'
    })
    assert response.status_code == 302  # Redirect to recipes page
    recipe = Recipe.query.get(recipe.id)
    assert recipe.title == 'Updated Recipe'


def test_delete_recipe(client, login):
    login()
    recipe = Recipe(title='Test Recipe', description='Test Description', ingredients='Test Ingredients', instructions='Test Instructions', created_by=1)
    db.session.add(recipe)
    db.session.commit()

    response = client.post(f'/recipes/{recipe.id}/delete')
    assert response.status_code == 302  # Redirect to recipes page
    recipe = Recipe.query.get(recipe.id)
    assert recipe is None


def test_search_recipe(client, login):
    login()
    recipe1 = Recipe(title='Chocolate Cake', description='Delicious chocolate cake', ingredients='Chocolate, Flour, Sugar', instructions='Mix and bake', created_by=1)
    recipe2 = Recipe(title='Vanilla Cake', description='Delicious vanilla cake', ingredients='Vanilla, Flour, Sugar', instructions='Mix and bake', created_by=1)
    db.session.add(recipe1)
    db.session.add(recipe2)
    db.session.commit()

    response = client.get('/search', query_string={'query': 'Chocolate'})
    assert response.status_code == 200
    assert b'Chocolate Cake' in response.data
    assert b'Vanilla Cake' not in response.data
