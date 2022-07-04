from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from src.database import User, db
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token

# Blueprint

users = Blueprint("users", __name__, url_prefix="/api/users")

# Routes


@users.get("/")
def getAll():
    users = db.session.query(User).filter()
    data = []
    for item in users:
        data.append({
            'id': item.id,
            'email': item.email,
            'firstName': item.firstName,
            'lastName': item.lastName
        })
    return (jsonify(data), 200)


@users.get("/")
def getAllQuery():
    users = db.session.execute("SELECT * from user")
    data = []
    for item in users:
        data.append({
            'id': item.id,
            'email': item.email,
            'firstName': item.firstName,
            'lastName': item.lastName
        })
    return (jsonify(data), 200)


@users.get("/<int:id>")
def getUser(id):

    user = db.session.query(User).filter(User.id == id).first()

    return (jsonify({
            'id': user.id,
            'email': user.email,
            'firstName': user.firstName,
            'lastName': user.lastName
            }), 200)


@users.post('/')
def create():
    email = request.json.get('email', '')
    password = request.json.get('password', '')
    firstName = request.json.get('firstName', '')
    lastName = request.json.get('lastName', '')

    if len(password) < 6:
        return jsonify({"error": "Password too short"}), 400

    if not validators.email(email):
        return jsonify({"error": "Email is not valid"}), 400

    if db.session.query(User).filter(User.email == email).first() is not None:
        return jsonify({"error": "Email is not taken"}), 409

    password_hash = generate_password_hash(password)

    user = User(email=email, password=password_hash,
                firstName=firstName, lastName=lastName)

    db.session.add(user)
    db.session.commit()

    return (jsonify({"message": "User created"}), 201)


@users.put('/<int:id>')
def update(id):
    email = request.json.get('email', '')
    firstName = request.json.get('firstName', '')
    lastName = request.json.get('lastName', '')

    user = db.session.query(User).filter(User.id == id).first()

    user.email = email
    user.firstName = firstName
    user.lastName = lastName
    db.session.commit()

    return (jsonify({
            'id': user.id,
            'email': user.email,
            'firstName': user.firstName,
            'lastName': user.lastName
            }), 200)


@users.delete('/<int:id>')
def delete(id):
    user = db.session.query(User).filter(User.id == id).first()

    if not user:
        return {"message": "Not found"}, 404

    db.session.delete(user)
    db.session.commit()

    return (jsonify({"result": True}), 200)


# Authentication
@users.post('/login')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = db.session.query(User).filter(User.email == email).first()
    if user:
        is_match = check_password_hash(user.password, password)
        if is_match:

            refreshToken = create_refresh_token(identity=user.id)
            accessToken = create_access_token(identity=user.id)

            return (jsonify({
                "accessToken": accessToken,
                "refreshToken": refreshToken
            }))

    return (jsonify({
        "error": 'Wrong credentials'
    }), 401)


@users.get("/protectedRoute")
@jwt_required()
def protectedRoute():
    userId = get_jwt_identity()

    user = db.session.query(User).filter(User.id == userId).first()

    return (jsonify({
            'id': user.id,
            'email': user.email,
            'firstName': user.firstName,
            'lastName': user.lastName
            }), 200)
