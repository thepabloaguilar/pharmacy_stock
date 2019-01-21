from flask import abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from ..model import PostgresSession
from ..model.customer import Customer
from ..security import auth_token_required
from ..parsers import create_customer_parser
from ..utils import _json_result


class CustomerResource(Resource):

    def _get_customer(self, customer_id):
        session = PostgresSession()

        customer = session.query(Customer) \
            .filter(Customer._id == customer_id).one_or_none()
        
        if not customer:
            abort(404, 'Customer not found')
        return customer

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
        print(f'CUSTOMER ID --> {customer._id}')
        return customer
    
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
    
    @auth_token_required()
    def post(self):
        args = create_customer_parser.parse_args()
        customer = self._create_customer(args)
        response = {
            'message': f'Customer "{customer.name}" was created successfuly'
        }
        return response, 201
    
    @auth_token_required(only_admin=True)
    def patch(self, customer_id):
        customer = self._inactive_active_customer(customer_id)
        action = 'activated' if customer.is_active else 'inactivated'
        return {'message': f'Customer "{customer.name}" {action}'}, 200


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
    def get(self):
        return _json_result(self._get_customers()), 200
