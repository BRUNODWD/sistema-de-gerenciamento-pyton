from flask import request, jsonify
from app import app, db
from app.models import User, Resource
from datetime import datetime

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], password=data['password'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'role': user.role} for user in users])

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    if user:
        user.username = data['username']
        user.password = data['password']
        user.role = data['role']
        db.session.commit()
        return jsonify({"message": "User updated"})
    return jsonify({"message": "User not found"}), 404

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"})
    return jsonify({"message": "User not found"}), 404

@app.route('/resources', methods=['POST'])
def create_resource():
    data = request.json
    new_resource = Resource(name=data['name'])
    db.session.add(new_resource)
    db.session.commit()
    return jsonify({"message": "Resource created"}), 201

@app.route('/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    return jsonify([{'id': resource.id, 'name': resource.name} for resource in resources])

@app.route('/resources/<int:id>', methods=['PUT'])
def update_resource(id):
    data = request.json
    resource = Resource.query.get(id)
    if resource:
        resource.name = data['name']
        db.session.commit()
        return jsonify({"message": "Resource updated"})
    return jsonify({"message": "Resource not found"}), 404

@app.route('/resources/<int:id>', methods=['DELETE'])
def delete_resource(id):
    resource = Resource.query.get(id)
    if resource:
        db.session.delete(resource)
        db.session.commit()
        return jsonify({"message": "Resource deleted"})
    return jsonify({"message": "Resource not found"}), 404

@app.route('/resources/allocate/<int:id>', methods=['POST'])
def allocate_resource(id):
    data = request.json
    resource = Resource.query.get(id)
    if resource and not resource.allocated_by:
        resource.allocated_by = data['user_id']
        resource.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        resource.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        db.session.commit()
        return jsonify({"message": "Resource allocated"})
    return jsonify({"message": "Resource not available or already allocated"}), 400
