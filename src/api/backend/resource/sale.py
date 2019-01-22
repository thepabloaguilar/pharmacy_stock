import requests

from datetime import datetime
from flask import abort
from flasgger import swag_from
from flask_restful import Resource
from sqlalchemy import func

from ..security import auth_token_required
from ..parsers import create_sale_parser, create_sale_item_parser
from ..utils import _json_result, request_to_myself
from ..model import PostgresSession
from ..model.customer import Customer
from ..model.sale import Sale
from ..model.sale_item import SaleItem


class SaleBaseResource(Resource):

    def _get_sale_items(self, sale_id):
        session = PostgresSession()
        return session.query(SaleItem).filter(SaleItem.sale_id == sale_id)

    def _get_sale(self, sale_id):
        session = PostgresSession()
        
        sale = session.query(Sale) \
            .filter(Sale._id == sale_id) \
            .filter(Sale.seller_id == self.user_info['user_id']) \
            .one_or_none()
        
        if not sale:
            abort(404, 'Sale not found')
        return sale
    
    def _update_medicine(self, medicine_id, quantity, action):
        data = {'quantity': quantity}
        headers = {'Content-Type': 'application/json'}
        r = request_to_myself(
            'patch',
            f'/medicine/{medicine_id}/{action}',
            data=data, headers=headers)

        if r.status_code == 404:
            abort(404, f'Medicine({medicine_id}) not found')
        return r.json()


class DeleteSaleResource(SaleBaseResource):

    def _make_sale_items_cancelation(self, sale_id):
        sale_items = self._get_sale_items(sale_id)
        base_url = f'/sale/{sale_id}/item'
        
        for sale_item in sale_items:
            request_to_myself('delete', f'{base_url}/{sale_item._id}')

    def _cancel_sale(self, sale_id):
        sale = self._get_sale(sale_id)
        session = PostgresSession()

        self._make_sale_items_cancelation(sale_id)

        session.query(Sale) \
            .filter(Sale._id == sale_id) \
            .update({Sale.status: 'CANCELLED'})
        session.commit()
        return sale
    
    @auth_token_required()
    @swag_from('../docs/sale/sale_delete.yml')
    def delete(self, sale_id):
        sale = self._cancel_sale(sale_id)
        return {'sale_id': sale._id, 'status': sale.status}, 200


class FinalizeSaleResource(SaleBaseResource):

    def _get_sale_items_sum_and_count(self, sale_id):
        session = PostgresSession()
        sum_and_count = session.query(
            func.count(SaleItem._id).label('count'),
            func.sum(SaleItem.final_price).label('sum')) \
            .filter(SaleItem.sale_id == sale_id) \
            .filter(SaleItem.is_cancelled == False).first()
        return sum_and_count
    
    def _make_sale_finalization(self, sale_id, amount):
        session = PostgresSession()

        session.query(Sale) \
        .filter(Sale._id == sale_id) \
        .update({
            Sale.amount: amount,
            Sale.transaction_date: datetime.now(),
            Sale.status: 'FINALIZED'
        })
        session.commit()

    def _finalize_sale(self, sale_id):
        sale = self._get_sale(sale_id)
        if sale.status != 'PENDING':
            abort(412, f'Sale({sale_id}) has been {sale.status}')

        sum_and_count = self._get_sale_items_sum_and_count(sale_id)
        if sum_and_count.count == 0:
            abort(412, f'Sale({sale_id}) does not have any items to compute')
        
        self._make_sale_finalization(sale_id, sum_and_count.sum)
        return sale

    @auth_token_required()
    @swag_from('../docs/sale/sale_finalize_patch.yml')
    def patch(self, sale_id):
        sale = self._finalize_sale(sale_id)
        response = {
            'sale_id': sale._id,
            'amount': sale.amount,
            'transaction_date': sale.transaction_date,
            'status': sale.status,
        }
        return _json_result(response), 200


class CreateSaleResource(Resource):

    def _verify_if_customer_exist(self, customer_id):
        session = PostgresSession()
        customer = session.query(Customer) \
            .filter(Customer._id == customer_id) \
            .filter(Customer.is_active == True).one_or_none()
        if not customer:
            abort(404, 'Customer not found')
        return customer

    def _create_sale(self, customer_id):
        self._verify_if_customer_exist(customer_id)
        session = PostgresSession()

        sale = Sale(
            customer_id=customer_id,
            seller_id=self.user_info['user_id']
        )
        session.add(sale)
        session.commit()
        return sale

    @auth_token_required()
    @swag_from('../docs/sale/sale_post.yml')
    def post(self):
        args = create_sale_parser.parse_args()
        sale = self._create_sale(args.customer_id)
        response = {
            'sale_id': sale._id,
            'date': sale.creation_date,
            'status': sale.status,
        }
        return _json_result(response), 201


class SaleItemResource(SaleBaseResource):

    def _get_sale_item(self, item_id):
        session = PostgresSession()

        sale_item = session.query(SaleItem) \
            .filter(SaleItem._id == item_id) \
            .one_or_none()
        
        if not sale_item:
            abort(404, f'Sale Item ({item_id}) not found')
        return sale_item
    
    def _delete_sale_item(self, sale_id, item_id):
        sale = self._get_sale(sale_id)
        if sale.status != 'PENDING':
            abort(400, 'Slae is no longer PENDING')

        sale_item = self._get_sale_item(item_id)
        session = PostgresSession()

        self._update_medicine(sale_item.medicine_id, sale_item.quantity, 'add')

        session.query(SaleItem) \
            .filter(SaleItem._id == item_id) \
            .update({
                SaleItem.is_cancelled: True
            })
        session.commit()
        return sale_item

    @auth_token_required()
    @swag_from('../docs/sale/sale_item_get.yml')
    def get(self, sale_id, item_id):
        self._get_sale(sale_id)
        sale_item = self._get_sale_item(item_id)
        _sale_item = {
            'id': sale_item._id,
            'sale_id': sale_item.sale_id,
            'medicine_id': sale_item.medicine_id,
            'current_medicine_price': sale_item.current_medicine_price,
            'quantity': sale_item.quantity,
            'final_price': sale_item.final_price,
            'is_cancelled': sale_item.is_cancelled,
            'creation_date': sale_item.creation_date,
        }
        return _json_result(_sale_item), 200
    
    @auth_token_required()
    @swag_from('../docs/sale/sale_item_delete.yml')
    def delete(self, sale_id, item_id):
        sale_item = self._delete_sale_item(sale_id, item_id)
        response = {
            'sale_item_id': sale_item._id,
            'is_cancelled': sale_item.is_cancelled
        }
        return response


class CreateSaleItemResource(SaleBaseResource):

    def _create_sale_item(self, sale_id, args):
        sale = self._get_sale(sale_id)
        if sale.status != 'PENDING':
            abort(412, 'Sale({sale_id}) is not PENDING')
        
        medicine_json = self._update_medicine(
            args.medicine_id, args.quantity, 'remove')

        session = PostgresSession()
        sale_item = SaleItem(
            sale_id=sale_id,
            medicine_id=medicine_json['medicine_id'],
            current_medicine_price=medicine_json['amount'],
            quantity=args.quantity,
            final_price=args.quantity * medicine_json['amount']
        )
        session.add(sale_item)
        session.commit()
        return sale_item

    @auth_token_required()
    @swag_from('../docs/sale/sale_item_post.yml')
    def post(self, sale_id):
        args = create_sale_item_parser.parse_args()
        sale_item = self._create_sale_item(sale_id, args)
        return {'sale_item_id': sale_item._id, 'quantity': args.quantity}


class SalesResource(Resource):

    def _get_sales(self):
        session = PostgresSession()
        sales = session.query(
            Sale._id,
            Sale.amount,
            Sale.transaction_date,
            Sale.customer_id,
            Sale.seller_id,
            Sale.status,
            Sale.creation_date
        )
        return [s._asdict() for s in sales]

    @auth_token_required()
    @swag_from('../docs/sale/sales_get.yml')
    def get(self):
        return _json_result(self._get_sales()), 200


class SaleItemsResource(SaleBaseResource):

    def _get_sale_items(self, sale_id):
        sale = self._get_sale(sale_id)
        session = PostgresSession()

        sale_items = session.query(
            SaleItem._id.label('id'),
            SaleItem.sale_id,
            SaleItem.medicine_id,
            SaleItem.current_medicine_price,
            SaleItem.quantity,
            SaleItem.final_price,
            SaleItem.is_cancelled,
            SaleItem.creation_date
        ).filter(SaleItem.sale_id == sale_id)
        return [si._asdict() for si in sale_items]

    @auth_token_required()
    @swag_from('../docs/sale/sale_items_get.yml')
    def get(self, sale_id):
        return _json_result(self._get_sale_items(sale_id))
