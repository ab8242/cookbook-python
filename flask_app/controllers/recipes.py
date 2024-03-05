from flask_app import app
from flask import render_template, redirect, request, session
# import entire file, rather than class, to avoid circular imports
from flask_app.models import recipe
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Recipe Controller


@app.route('/new', methods=['POST', 'GET'])
def create_new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if request.method == 'GET':
        return render_template('add_new_recipe.html')
    if recipe.Recipe.add_recipe_to_database(request.form):
        return redirect('/addIngredients')
    return redirect('/new')

# Read Users Controller


@app.route('/show/<int:id>')
def show_recipe_by_id(id):
    if 'user_id' not in session:
        return redirect('/')
    one_recipe = recipe.Recipe.view_all_recipes_with_authors(id)
    return render_template('show_car.html', one_recipe=one_recipe)

# Update Users Controller


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit_recipe_by_author(id):
    if 'user_id' not in session:
        return redirect('/')
    if request.method == 'GET':
        one_recipe = recipe.Recipe.view_recipe_by_id(id)
        return render_template('edit_recipe.html', one_recipe=one_recipe)
    if request.method == 'POST':
        recipe.Recipe.edit_recipe_by_author(request.form)
        return redirect('/dashboard')
    return redirect(f"/edit/recipe/{request.form['id']}")

# Delete Users Controller


# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal


# How to use path variables:
# @app.route('/<int:id>')                                   The variable must be in the path within angle brackets
# def index(id):                                            It must also be passed into the function as an argument/parameter
#     user_info = user.User.get_user_by_id(id)              The it will be able to be used within the function for that route
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.

# Render template is a function that takes in a template name in the form of a string, then any number of named arguments containing data to pass to that template where it will be integrated via the use of jinja
# Redirect redirects from one route to another, this should always be done following a form submission. Don't render on a form submission.
