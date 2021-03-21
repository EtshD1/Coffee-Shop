import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
import sys
from flask_cors import CORS

from .database import db_drop_and_create_all, setup_db, Drink, db
from .auth import AuthError, requires_permission

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO:Done uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES

# @TODO:Done implement endpoint
#     GET /drinks
#         it should be a public endpoint
#         it should contain only the drink.short() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
#         or appropriate status code indicating reason for failure


@app.route("/drinks")
def drinks():
    try:
        drinksList = Drink.query.all()
        return jsonify({
            "success": True,
            "drinks": [drink.short() for drink in drinksList]
        })
    except:
        db.session.rollback()
        print(sys.exc_info())
        abort(400)
    finally:
        db.session.close()


# @TODO:Done implement endpoint
#     GET /drinks-detail
#         it should require the 'get:drinks-detail' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
#         or appropriate status code indicating reason for failure
@app.route("/drinks-detail")
@requires_permission("get:drinks-detail")
def drinkDetails(jwt):
    try:
        drinksList = Drink.query.all()
        return jsonify({
            "success": True,
            "drinks": [drink.long() for drink in drinksList]
        })
    except:
        db.session.rollback()
        print(sys.exc_info())
        abort(400)
    finally:
        db.session.close()


# @TODO:Done implement endpoint
#     POST /drinks
#         it should create a new row in the drinks table
#         it should require the 'post:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
#         or appropriate status code indicating reason for failure
@app.route("/drinks", methods=['POST'])
@requires_permission("post:drinks")
def createDrink(jwt):
    try:
        body = request.get_json()

        print(body)

        title = body.get('title')
        recipe = body.get('recipe')

        newDrink = Drink(
            title=title,
            recipe=recipe
        )

        newDrink.insert()
        return jsonify({'success': True, "drinks": newDrink.long()})
    except:
        db.session.rollback()
        print(sys.exc_info())
        abort(400)
    finally:
        db.session.close()


# @TODO implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure
@app.route("/drinks/<id>", methods=['PATCH'])
@requires_permission("patch:drinks")
def patchDrink(jwt, id):
    try:
        print(jwt)
        print(id)
        body = request.get_json()

        title = body.get('title', None)
        recipe = body.get('recipe', None)
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink:
            if title:
                drink.title = title
            if recipe:
                drink.recipe = recipe
            drink.update()
            return jsonify({'success': True, "drinks": drink.long()})
        else:
            return jsonify({'success': False, "info": "Drink not found"})
    except:
        db.session.rollback()
        print(sys.exc_info())
        abort(400)
    finally:
        db.session.close()


# @TODO implement endpoint
#     DELETE /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should delete the corresponding row for <id>
#         it should require the 'delete:drinks' permission
#     returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
#         or appropriate status code indicating reason for failure
@app.route("/drinks/<id>", methods=['DELETE'])
@requires_permission("delete:drinks")
def deleteDrink(jwt, id):
    try:
        print(jwt)
        print(id)
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink:
            drink.delete()
            return jsonify({'success': True, "delete": id})
        else:
            return jsonify({'success': False, "info": "Drink not found"})
    except:
        db.session.rollback()
        print(sys.exc_info())
        abort(400)
    finally:
        db.session.close()


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


# @TODO:Done implement error handlers using the @app.errorhandler(error) decorator
#     each error handler should return (with approprate messages):
#              jsonify({
#                     "success": False,
#                     "error": 404,
#                     "message": "resource not found"
#                     }), 404

# @TODO:Done implement error handler for 404
#     error handler should conform to general task above
@app.errorhandler(404)
def notFound(error):
    print(error)
    jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


@app.errorhandler(403)
def forbidden(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403


@app.errorhandler(400)
def badRequest(error):
    print(error)
    return jsonify({
        'success': False,
        'info': 'Bad request',
        'error': 400
    }), 400


# @TODO:Done implement error handler for AuthError
#     error handler should conform to general task above
@app.errorhandler(401)
def unauthorized(error):
    print(error)
    return jsonify({
        'success': False,
        'info': 'Unauthorized',
        'error': 401
    }), 401
