
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import recipe
# import re
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat names, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the name for what it needs, ideally.


class Ingredients:
    db = "cookbook_schema"  # which database are you using for this project

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.measurement = data['measurement']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.in_recipe = []
        self.lister = None

        # What changes need to be made above for this project?
        # What needs to be added here for class association?

    # Create Users Names
    @classmethod
    def add_ingredients(cls, ingredient_data):
        if not cls.validate_ingredient_info(ingredient_data):
            return False
        query = """
                INSERT INTO ingredients (name, measurement)
                VALUES (%(name)s, %(measurement)s)
                ;"""
        new_ingredient = connectToMySQL(
            cls.db).query_db(query, ingredient_data)
        return new_ingredient
    # Read Users Names

    @classmethod
    def view_all_cars_with_sellers(cls):
        query = """
                SELECT * FROM cars
                JOIN users
                ON cars.user_id = users.id
                ;"""
        results = connectToMySQL(cls.db).query_db(query)
        cars_sellers = []
        for result in results:
            one_car = cls(result)
            one_car.lister = user.User({
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']
            })
            cars_sellers.append(one_car)
        return cars_sellers

    @classmethod
    def view_car_by_id(cls, id):
        data = {'id': id}
        query = """
                SELECT * FROM cars
                WHERE id = %(id)s
                ;"""
        view_car = connectToMySQL(cls.db).query_db(query, data)
        return cls(view_car[0])

    @classmethod
    def view_car_by_id_with_seller(cls, id):
        data = {'id': id}
        query = """
                SELECT * FROM cars
                JOIN users
                ON cars.user_id = users.id
                WHERE cars.id = %(id)s
                ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        one_car_data = results[0]
        one_car_obj = Car(one_car_data)
        seller = user.User({
            'id': one_car_data['users.id'],
            'first_name': one_car_data['first_name'],
            'last_name': one_car_data['last_name'],
            'email': one_car_data['email'],
            'password': one_car_data['password'],
            'created_at': one_car_data['users.created_at'],
            'updated_at': one_car_data['users.updated_at']
        })
        one_car_obj.lister = seller
        return one_car_obj

    @classmethod
    def edit_car_by_seller(cls, car_data):
        if not cls.validate_car_info(car_data):
            return False
        query = """
                UPDATE cars SET
                name=%(name)s, 
                measurement=%(measurement)s,
                year=%(year)s,
                description=%(description)s,
                user_id=%(user_id)s,
                price=%(price)s
                WHERE id = %(id)s
                ;"""
        updated_car = connectToMySQL(cls.db).query_db(query, car_data)
        return updated_car
    # Delete Users Names

    @classmethod
    def purchased_car_by_id(cls, id):
        data = {'id': id}
        query = """
                DELETE FROM cars
                WHERE id = %(id)s
                ;"""
        connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_ingredient_info(data):
        is_valid = True
        if len(data['name']) < 2:
            flash(
                'Ingredients name must be longer than 2 characters!!  Please try again!')
            is_valid = False
        if len(data['measurement']) < 2:
            flash('Measurement must be longer than 2 characters!!  Please try again!')
            is_valid = False
        return is_valid
