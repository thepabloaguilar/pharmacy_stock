import flask_restful

from flask import Blueprint
from .resource import pharmacy_user, login, provider, medicine


api_bp = Blueprint('backend', __name__)
api = flask_restful.Api(api_bp)

api.add_resource(
    pharmacy_user.PharmacyUserResource,
    '/user', '/user/<int:user_id>')
api.add_resource(pharmacy_user.PharmacyUsersResource, '/users')

api.add_resource(login.Login, '/login')

api.add_resource(
    provider.ProviderResource,
    '/provider', '/provider/<int:provider_id>')
api.add_resource(provider.ProvidersResource, '/providers')

api.add_resource(
    medicine.MedicineResource,
    '/medicine', '/medicine/<int:medicine_id>')
api.add_resource(medicine.MedicinesResource, '/medicines')
api.add_resource(medicine.UploadMedicinesResource, '/medicines/upload')
