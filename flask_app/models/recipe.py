
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
# import re
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat titles, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the title for what it needs, ideally.


class Recipe:
    db = "cookbook_schema"  # which database are you using for this project

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.total_time = data['total_time']
        self.prep_time = data['prep_time']
        self.cook_time = data['cook_time']
        self.serving_size = data['serving_size']
        self.directions = data['directions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.lister = None
        self.ingredients = []

        # What changes need to be made above for this project?
        # What needs to be added here for class association?

    # Create Recipe
    @classmethod
    def add_recipe_to_database(cls, recipe_data):
        if not cls.validate_recipe_info(recipe_data):
            return False
        query = """
                INSERT INTO recipes ( title, total_time, prep_time, cook_time, serving_size, directions, user_id )
                VALUES ( %(title)s, %(total_time)s, %(prep_time)s, %(cook_time)s, %(serving_size)s, %(directions)s, %(user_id)s )
                ;"""
        new_recipe = connectToMySQL(cls.db).query_db(query, recipe_data)
        return new_recipe

    # View All Recipes on Dashboard
    @classmethod
    def view_all_recipes_with_authors(cls):
        query = """
                SELECT * FROM recipes
                JOIN users
                ON recipes.user_id = users.id
                ;"""
        results = connectToMySQL(cls.db).query_db(query)
        recipes_authors = []
        for result in results:
            one_recipe = cls(result)
            one_recipe.lister = user.User({
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'user_name': result['user_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at']
            })
            recipes_authors.append(one_recipe)
        return recipes_authors

    @classmethod
    def view_recipe_by_id(cls, id):
        data = {'id': id}
        query = """
                SELECT * FROM recipes
                WHERE id = %(id)s
                ;"""
        view_recipe = connectToMySQL(cls.db).query_db(query, data)
        return cls(view_recipe[0])

    @classmethod
    def view_recipe_by_id_with_author(cls, id):
        data = {'id': id}
        query = """
                SELECT * FROM recipes
                JOIN users
                ON recipes.user_id = users.id
                WHERE recipes.id = %(id)s
                ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        one_recipe_data = results[0]
        one_recipe_obj = Recipe(one_recipe_data)
        author = user.User({
            'id': one_recipe_data['users.id'],
            'first_name': one_recipe_data['first_name'],
            'last_name': one_recipe_data['last_name'],
            'user_name': one_recipe_data['user_name'],
            'email': one_recipe_data['email'],
            'password': one_recipe_data['password'],
            'created_at': one_recipe_data['users.created_at'],
            'updated_at': one_recipe_data['users.updated_at']
        })
        one_recipe_obj.lister = author
        return one_recipe_obj

    @classmethod
    def edit_recipe_by_author(cls, recipe_data):
        if not cls.validate_recipe_info(recipe_data):
            return False
        query = """
                UPDATE recipes SET
                title=%(title)s, 
                total_time=%(total_time)s,
                prep_time=%(prep_time)s,
                cook_time=%(cook_time)s,
                user_id=%(user_id)s,
                serving_size=%(serving_size)s
                directions=%(directions)s
                WHERE id = %(id)s
                ;"""
        updated_recipe = connectToMySQL(cls.db).query_db(query, recipe_data)
        return updated_recipe
    # Delete Users Titles

    @classmethod
    def purchased_recipe_by_id(cls, id):
        data = {'id': id}
        query = """
                DELETE FROM recipes
                WHERE id = %(id)s
                ;"""
        connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_recipe_info(data):
        is_valid = True
        if len(data['title']) < 2:
            flash('Recipe title must be longer than 2 characters!!  Please try again!')
            is_valid = False
        if int(data['total_time']) == 0:
            flash(
                'Recipe total time must be longer than 2 characters!!  Please try again!')
            is_valid = False
        if int(data['prep_time']) == 0:
            flash(
                ' Recipe prep time can not be 0!  Please put in the correct prep time!!')
            is_valid = False
        if int(data['cook_time']) == 0:
            flash(
                'Recipe cook time cannot be 0!!  Please add a cook time!')
            is_valid = False
        if int(data['serving_size']) == 0:
            flash(
                'Recipe serving size cannot be 0!!  Please add the serving size of your recipe!')
            is_valid = False
        if len(data['directions']) == 0:
            flash(
                'Directions cannot be left blank.  Please add the directions to the form.'
            )
        elif len(data['directions']) < 15:
            flash(
                'Need more directions.  We all do not know what we are doing!')
            is_valid = False
        return is_valid
