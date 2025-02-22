from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

# Edited this function to account for a string query for hobby
# when searching for a contact by String. If a string query is given
# in the form of a hobby, the function get_contacts_by_hobby() is called
# with the given hobby. 
@app.route("/contacts", methods=['GET'])
def get_all_contacts():

    hobby = request.args.get('hobby')

    if(hobby != ""):
        return get_contacts_by_hobby(hobby)

    else:
        return create_response({"contacts": db.get('contacts')})

# Edited for use to delete contacts instead of shows.
# Previous @app.route and function header commented out below,
# replaced with relevant @app.route and function header for 
# the contact problem.
#@app.route("/shows/<id>", methods=['DELETE'])
#def delete_show(id):
@app.route("/contacts/<id>", methods=['DELETE'])
def delete_contact(id):
    if db.getById('contacts', int(id)) is None:
        return create_response(status=404, message="No contact with this id exists")
    db.deleteById('contacts', int(id))
    return create_response(message="Contact deleted")


# TODO: Implement the rest of the API here!

@app.route("/contacts/<id>", methods=['GET'])
def get_single_contact_from_id(id):

    if db.getById('contacts', int(id)) is None:
        return create_response(status=404, message="The contact with id " + str(id) + " was not found.")

    return create_response({'contact': db.getById('contacts', int(id))})

#@app.route("/contacts", methods=['GET'])


def get_contacts_by_hobby(hobby):

    found_by_hobby = []
    all_contacts = db.get('contacts')

    for contact in all_contacts:
        if contact['hobby'] == hobby:
            found_by_hobby.append(contact)

    if(found_by_hobby != []):
        return create_response({'contacts': found_by_hobby})

    else:
        return create_response(status=404, message="There were no contacts with hobby " + hobby + " found.")

@app.route("/contacts", methods=['POST'])
def create_contact_with_info():

    input_info = request.json

    missing = ''
    num_missing = 0

    check_name = (('name' in input_info) and (input_info['name'] != ''))
    check_nickname = (('nickname' in input_info) and (input_info['nickname'] != ''))
    check_hobby = (('hobby' in input_info) and (input_info['hobby'] != ''))

    if(check_name and check_nickname and check_hobby):
        contact = db.create('contacts', {'name': input_info['name'], 'nickname': input_info['nickname'], 'hobby': input_info['hobby']})
        return create_response(status=201, data={'contact': contact})

    if(not(check_name)):
        missing += 'a name'
        num_missing += 1

    if(not(check_nickname)):
        if(num_missing == 1):
            missing += ', '

        missing += 'a nickname'
        num_missing += 1

    if(not(check_hobby)):
        if(num_missing > 0):
            missing += ', '

        missing += 'a hobby'

    return create_response(status=404, message = "You are missing " + missing + ". Please revise your input and try again!")

@app.route("/contacts/<id>", methods=['PUT'])
def update_contact_with_info(id):

    input_info = request.json

    check_name = (('name' in input_info) and (input_info['name'] != ''))
    check_hobby = (('hobby' in input_info) and (input_info['hobby'] != ''))

    if db.getById('contacts', int(id)) is None:
        return create_response(status=404, message="The contact with id " + str(id) + " was not found.")

    if(check_name):
        db.updateById('contacts', int(id), {'name': input_info['name']})

    if(check_hobby):
        db.updateById('contacts', int(id), {'hobby': input_info['hobby']})

    return create_response({'contact': db.getById('contacts', int(id))})


###################################################
## Part 6 was included in the initial code base, ##
## was updated above for use on contacts instead ##
## of shows.                                     ##
###################################################
        

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
