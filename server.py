from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)


try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.company
    mongo.server_info() # trigger exception if cannot connect to db

except:
    print("ERROR - Cannot connect to db")
########################################################

# Data insert operation

@app.route('/insert_users', methods=['POST'])
def create_user():
    try:
        user = {
            "firstName":request.form["firstName"],
            "lastName": request.form["lastName"],
            "email": request.form["email"],
            "mobile": request.form["mobile"]
        }
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        # for attr in dir(dbResponse):
        #     print(attr)
        return Response(
            response= json.dumps(
                {"message":"user created",
                 "id":f"{dbResponse.inserted_id}"
                 }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:

        print(ex)
        return Response(response= json.dumps({"message":"sorry! unable to insert the data"}), status=500, mimetype="application/json")



# Retrive operation

@app.route("/get_users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response= json.dumps(data),
            status=500,
            mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message":"cannot read users"}), status=500, mimetype="application/json")



# Update operation

@app.route("/update_users/<id>", methods=["PATCH"])
def update_users(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "firstName":request.form["firstName"],
                "lastName": request.form["lastName"]
            }}
        )
        if dbResponse.modified_count == 1:
            return Response(
                response= json.dumps({"message":"user updated", "id":f"{id}"}),
                status=200,
                mimetype="application/json"
            )

        return Response(
            response= json.dumps({"message":"nothing to update"}),
            status=404,
            mimetype="application/json"
        )


    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message":"user not found"}), status=500, mimetype="application/json")

# delete operation

@app.route("/delete_users/<id>", methods=["DELETE"])
def delete_users(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response( response= json.dumps({"message":"user deleted", "id":f"{id}"}),status=200,mimetype="application/json")

        return Response(response= json.dumps({"message":"user not found", "id":f"{id}"}),status=404,mimetype="application/json")

    except Exception as ex:
        return Response(response= json.dumps({"message":"sorry cannot delete the user"}), status=500, mimetype="application/json")


###########################################

if __name__ == '__main__':
    app.run(port=5000, debug=True)
