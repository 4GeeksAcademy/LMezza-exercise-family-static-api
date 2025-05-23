"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    if members == []:
        return jsonify({"msg": "there are no members in this family"}), 400

    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):

    member = jackson_family.get_member(id)

    if member == None:
        return jsonify({"msg": "this member doesn't exist"}), 400
    
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def handle_post():
    
    request_body = request.json
    if not all(key in request_body for key in ["first_name", "age", "lucky_numbers"]):
         return jsonify({"msg": "missing information"}), 400
    
    member = jackson_family.add_member(request_body)
    return jsonify(member), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def handle_delete_member(member_id):
    
    delete_member = jackson_family.delete_member(member_id)
    if delete_member == None:
        return jsonify({"msg": "this member does not exist"}), 400
    return jsonify({"done": "True"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
