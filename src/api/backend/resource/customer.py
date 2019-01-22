import io
import csv

from flask import abort, send_file
from flasgger import swag_from
from flask_restful import Resource
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from ..model import PostgresSession
from ..model.customer import Customer
from ..model.sale import Sale
from ..model.sale_item import SaleItem
from ..model.medicine import Medicine
from ..model.medicine_type import MedicineType
from ..model.provider import Provider
from ..security import auth_token_required
from ..parsers import create_customer_parser
from ..utils import _json_result


class CustomerBaseResource(Resource):

    def _get_customer(self, customer_id):
        session = PostgresSession()

        customer = session.query(Customer) \
            .filter(Customer._id == customer_id).one_or_none()
        
        if not customer:
            abort(404, 'Customer not found')
        return customer


class CustomerResource(CustomerBaseResource):
    
    def _inactive_active_customer(self, customer_id):
        customer = self._get_customer(customer_id)
        session = PostgresSession()
        
        session.query(Customer) \
        .filter(Customer._id == customer_id) \
        .update({
            Customer.is_active: not customer.is_active
        })
        session.commit()

        return customer

    @auth_token_required()
    @swag_from('../docs/customer/customer_get.yml')
    def get(self, customer_id):
        customer = self._get_customer(customer_id)
        _customer = {
            'id': customer._id,
            'name': customer.name,
            'telephone': customer.telephone,
            'tax_id': customer.tax_id,
            'is_active': customer.is_active,
            'genre': customer.genre,
            'creation_date': customer.creation_date,
        }
        return _json_result(_customer)
    
    @auth_token_required(only_admin=True)
    @swag_from('../docs/customer/customer_patch.yml')
    def patch(self, customer_id):
        customer = self._inactive_active_customer(customer_id)
        action = 'activated' if customer.is_active else 'inactivated'
        return {'message': f'Customer "{customer.name}" {action}'}, 200


class CreateCustomerResource(Resource):

    def _create_customer(self, informations):
        session = PostgresSession()

        customer = Customer(
            name=informations.name,
            telephone=informations.telephone,
            tax_id=informations.tax_id,
            genre=informations.genre
        )

        try:
            session.add(customer)
            session.commit()
        except IntegrityError:
            session.rollback()
            abort(412, '"tax_id" already exists')
        return customer

    @auth_token_required()
    @swag_from('../docs/customer/customer_post.yml')
    def post(self):
        args = create_customer_parser.parse_args()
        customer = self._create_customer(args)
        response = {
            'message': f'Customer "{customer.name}" was created successfuly'
        }
        return response, 201


class CustomersResource(Resource):

    def _get_customers(self):
        session = PostgresSession()
        customers = session.query(
            Customer._id.label('id'),
            Customer.name,
            Customer.telephone,
            Customer.tax_id,
            Customer.is_active,
            Customer.genre,
            Customer.creation_date
        )
        return [c._asdict() for c in customers]

    @auth_token_required()
    @swag_from('../docs/customer/customers_get.yml')
    def get(self):
        return _json_result(self._get_customers()), 200


class CustomerMedicines(CustomerBaseResource):

    def _get_customer_medicines(self, customer_id):
        self._get_customer(customer_id)
        session = PostgresSession()

        medicines = session.query(
            Sale.transaction_date,
            Medicine.name,
            SaleItem.current_medicine_price.label('price'),
            SaleItem.quantity,
            func.concat(
                Medicine.dosage, '(', MedicineType.unit, ')'
            ).label('usage'),
            MedicineType.description,
            Provider.name.label('provider_name')
        ).select_from(Sale) \
        .join(SaleItem, SaleItem.sale_id == Sale._id) \
        .join(Medicine, Medicine._id == SaleItem.medicine_id) \
        .join(MedicineType, MedicineType._id == Medicine.medicine_type_id) \
        .join(Provider, Provider._id == Medicine.provider_id) \
        .filter(Sale.customer_id == customer_id) \
        .filter(Sale.status == 'FINALIZED') \
        .filter(SaleItem.is_cancelled == False)
        return [m._asdict() for m in medicines]

    @auth_token_required()
    def get(self, customer_id):
        return _json_result(self._get_customer_medicines(customer_id))


class CustomerMedicinesDownloadResource(CustomerMedicines):

    def _to_csv(self, medicines):
        header = [
            'transaction_date', 'name', 'price',
            'quantity', 'usage', 'description', 'provider_name'
        ]
        _io = io.StringIO()

        writer = csv.DictWriter(_io, fieldnames=header)
        writer.writeheader()
        writer.writerows(medicines)

        _io_bytes = io.BytesIO()
        _io_bytes.write(_io.getvalue().encode('utf-8'))
        _io_bytes.seek(0)
        return _io_bytes

    def get(self, customer_id):
        medicines = self._get_customer_medicines(customer_id)
        return send_file(
            self._to_csv(medicines),
            mimetype='text/csv',
            as_attachment=True,
            attachment_filename=f'{customer_id}.csv')
