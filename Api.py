from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///universities.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    accreditation = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"University('{self.name}', '{self.province}', '{self.city}')"

class UniversitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'province', 'city', 'status', 'accreditation')

university_schema = UniversitySchema()
universities_schema = UniversitySchema(many=True)

@app.route('/universities', methods=['GET'])
def get_universities():
    all_universities = University.query.all()
    result = universities_schema.dump(all_universities)
    return jsonify(result)

@app.route('/universities/<id>', methods=['GET'])
def get_university(id):
    university = University.query.get(id)
    if not university:
        return jsonify({'error': 'University not found'}), 404
    return jsonify(university_schema.dump(university))

@app.route('/universities', methods=['POST'])
def create_university():
    name = request.json['name']
    province = request.json['province']
    city = request.json['city']
    status = request.json['status']
    accreditation = request.json['accreditation']

    new_university = University(name=name, province=province, city=city, status=status, accreditation=accreditation)
    db.session.add(new_university)
    db.session.commit()

    return jsonify(university_schema.dump(new_university)), 201

@app.route('/universities/<id>', methods=['PUT'])
def update_university(id):
    university = University.query.get(id)
    if not university:
        return jsonify({'error': 'University not found'}), 404

    university.name = request.json['name']
    university.province = request.json['province']
    university.city = request.json['city']
    university.status = request.json['status']
    university.accreditation = request.json['accreditation']

    db.session.commit()
    return jsonify(university_schema.dump(university))

@app.route('/universities/<id>', methods=['DELETE'])
def delete_university(id):
    university = University.query.get(id)
    if not university:
        return jsonify({'error': 'University not found'}), 404

    db.session.delete(university)
    db.session.commit()
    return jsonify({'message': 'University deleted'})

if __name__ == '__main__':
    if not os.path.exists('universities.db'):
        db.create_all()
    app.run(debug=True)
