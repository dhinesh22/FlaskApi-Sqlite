from flask import Blueprint
from flask_restful import Api
from service.Create import Creates, Volume, Keypair

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Creates, '/create')
api.add_resource(Volume, '/volume')
api.add_resource(Keypair, '/keypair')

