import os
import logging
from flask import Flask, jsonify, request, abort
from service.common import status  # HTTP Status Codes
from service.models import db, Account, init_db

app = Flask(__name__)

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app)

######################################################################
# LIST ALL ACCOUNTS
######################################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """
    List all Accounts
    This endpoint will list all Accounts
    """
    app.logger.info("Request to list Accounts")

    accounts = Account.all()
    # account_list = [account.serialize() for account in accounts]

    # app.logger.info("Returning [%s] accounts", len(account_list))
    return jsonify(accounts), status.HTTP_200_OK

######################################################################
# READ AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    """
    Reads an Account
    This endpoint will read an Account based on the account_id that is requested
    """
    app.logger.info("Request to read an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    return jsonify(account.serialize()), status.HTTP_200_OK

######################################################################
# CREATE AN ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_account():
    """
    Create an Account
    This endpoint will create an Account
    """
    # app.logger.info("Request to create an Account")
    
    account_data = request.get_json()
    account = Account()
    account.deserialize(account_data)
    account.save()

    app.logger.info("Account created")
    return jsonify(account.serialize()), status.HTTP_201_CREATED, {'Location': f'/accounts/{account.id}'}

######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """
    Update an Account
    This endpoint will update an Account based on the posted data
    """
    app.logger.info("Request to update an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    account.deserialize(request.get_json())
    account.update()

    return jsonify(account.serialize()), status.HTTP_200_OK

######################################################################
# DELETE AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """
    Delete an Account
    This endpoint will delete an Account based on the account_id that is requested
    """
    app.logger.info("Request to delete an Account with id: %s", account_id)

    account = Account.find(account_id)
    if account:
        account.delete()

    return '', status.HTTP_204_NO_CONTENT
