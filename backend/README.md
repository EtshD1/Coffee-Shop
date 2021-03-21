# Trivia API Backend

## Installing Dependencies
To start up this project, please make sure that python is installed, as well as these dependencies:
- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM will be used to handle the database interactions.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests from our frontend server.
- [JOSE](https://python-jose.readthedocs.io/en/latest/) is JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the this directory run command:
```
flask run
```
You can also edit environmental variables in the `.env` file.

## Endpoints

### GET /drinks
- Permission: None
- Returns: An object with the list of drink.
- Response:
```json
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "Water3"
        }
    ],
    "success": true
}
```
### GET /drinks-detail
- Permission: get:drinks-detail
- Returns: An object with the list of detailed drinks.
- Response:
```json
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water3"
        }
    ],
    "success": true
}
```
### POST /drinks
- Permission: post:drinks
- Returns: An object with the created drink details.
- Response:
```json
{
    "drinks": {
        "id": 1,
        "recipe": [
            {
                "color": "blue",
                "name": "Water",
                "parts": 1
            }
        ],
        "title": "Water3"
    },
    "success": true
}
```
### PATCH /drinks/(id)
- Permission: patch:drinks
- Returns: An object with the patched drink details.
- Response:
```json
{
    "drinks": {
        "id": 1,
        "recipe": [
            {
                "color": "blue",
                "name": "Water",
                "parts": 1
            }
        ],
        "title": "Water5"
    },
    "success": true
}
```
### DELETE /drinks/(id)
- Permission: delete:drinks
- Returns: An object with the deleted id.
- Response:
```json
{
    "delete": "1",
    "success": true
}
```
## Error Handling
If a error occurs, and object would be sent with the info about the error. ex:
```json
{
  "success": false,
  "error": 404,
  "message": "Not found"
}
```