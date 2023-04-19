from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model

class Roads:
    def __init__(self, data):
        self.id = data['id']
        self.date = data['date']
        self.origin = data['origin']
        self.destination = data['destination']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.post_by = None
        
#?=========create a classmethod========
    @classmethod
    def roads_utv(cls,data):
        query = """
            INSERT INTO off_roads (origin,destination,user_id,date)
            VALUES (%(origin)s,%(destination)s,%(user_id)s,%(date)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
        
#?===========read all==========
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM off_roads
            JOIN users 
            ON off_roads.user_id = users.id;

        """
        results = connectToMySQL(DATABASE).query_db(query)
        print (results)

        all_roads = []
        if results:
            for row in results:
                the_roads = cls(row)
                user_data = {
                    'id' : row['user_id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at'], 
                    **row
                }
                this_user = user_model.User(user_data)
                the_roads.create_by = this_user
                all_roads.append(the_roads)
        return all_roads
    
#?=======read one========
# 
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM off_roads
            JOIN users 
            ON off_roads.user_id = users.id
            WHERE off_roads.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        print (results)
        this_roads = cls(results[0])
        for row in results:
            user_data = {
                **row,
                'id' : row['user_id'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'] 
            }  
            this_user = user_model.User(user_data)
            this_roads.post_by = this_user
            return this_roads
        return False  

#?=======update========
    # @classmethod
    # def update_roads(cls,data):
    #     query = """
    #         UPDATE off_roads
    #         SET origin = %(origin)s,
    #         destination = %(destination)s,
    #         date = %(date)s
    #         WHERE id = %(id)s;
    #     """
    #     return connectToMySQL(DATABASE).query_db(query,data)

#?=======delete========

    @classmethod
    def delete(cls,data):
        query = """
            DELETE FROM off_roads
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)
        

#?=======validator=======


    @staticmethod
    def validator(data):
        is_valid =True
        print(data)
        # if len(data['name']) < 1:
        #     is_valid = False
        #     flash("Must have a Name")
        # if len(data['place']) < 1:
        #     is_valid = False
        #     flash("Must have a Place")
        if len(data['date']) < 1:
            is_valid = False
            flash("Must type a Date")
        if len(data['origin']) < 1:
            is_valid = False
            flash("Must create a Origin")
        if len(data['destination']) < 1:
            is_valid = False
            flash("Must type a Destination")

        return is_valid  