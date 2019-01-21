import pandas as pd

from flask import abort
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from ..security import auth_token_required
from ..model import PostgresSession
from ..model.medicine import Medicine
from ..utils import _json_result
from ..parsers import create_medicine_parser, upload_medicine_csv, \
    change_medicine_stock_parser

class MedicineResource(Resource):

    def _get_medicine(self, medicine_id):
        session = PostgresSession()

        medicine = session.query(Medicine) \
            .filter(Medicine._id == medicine_id)
        
        if not self.user_info['is_admin']:
            medicine = medicine.filter(Medicine.is_active == True)

        medicine = medicine.one_or_none()
        if not medicine:
            abort(404, 'Medicine not found')
        return medicine

    def _create_medicine(self, informations):
        session = PostgresSession()
        medicine = Medicine(
            name=informations.name,
            medicine_type_id=informations.medicine_type_id,
            dosage=informations.dosage,
            amount=informations.amount,
            quantity=informations.quantity,
            provider_id=informations.provider_id
        )
        try:
            session.add(medicine)
            session.commit()
        except IntegrityError:
            session.rollback()
            abort(412, '"provider_id" or "medicine_type_id" is wrong')
        return medicine
    
    def _inactive_active_medicine(self, medicine_id):
        medicine = self._get_medicine(medicine_id)
        session = PostgresSession()

        session.query(Medicine) \
        .filter(Medicine._id == medicine_id) \
        .update({
            Medicine.is_active: not medicine.is_active
        })
        session.commit()

        return medicine


    @auth_token_required()
    def get(self, medicine_id):
        medicine = self._get_medicine(medicine_id)
        _medicine = {
            'id': medicine._id,
            'name': medicine.name,
            'medicine_type_id': medicine.medicine_type_id,
            'dosage': medicine.dosage,
            'amount': medicine.amount,
            'quantity': medicine.quantity,
            'provider_id': medicine.provider_id,
            'is_active': medicine.is_active,
            'creation_date': medicine.creation_date,
        }
        return _json_result(_medicine)
    
    @auth_token_required(only_admin=True)
    def post(self):
        args = create_medicine_parser.parse_args()
        self._create_medicine(args)
        return {'message': f'Medicine "{args.name}" was created successfuly'}, 201
    
    @auth_token_required(only_admin=True)
    def patch(self, medicine_id):
        medicine = self._inactive_active_medicine(medicine_id)
        action = 'activated' if medicine.is_active else 'inactivated'
        return {'message': f'Medicine "{medicine.name}" {action}'}, 200


class MedicinesResource(Resource):

    def _get_medicines(self):
        session = PostgresSession()

        medicines = session.query(
            Medicine._id.label('id'),
            Medicine.name,
            Medicine.medicine_type_id,
            Medicine.dosage,
            Medicine.amount,
            Medicine.provider_id,
            Medicine.is_active,
            Medicine.creation_date
        )
        return [m._asdict() for m in medicines]

    @auth_token_required()
    def get(self):
        return _json_result(self._get_medicines())


class UploadMedicinesResource(Resource):

    def _read_csv(self, _file, sep=';'):
        headers = {
            'name', 'medicine_type_id', 'dosage',
            'amount', 'quantity', 'provider_id'
        }
        csv = pd.read_csv(_file, sep=sep)
        if len((headers - set(csv))) != 0:
            abort(412, 'Invalid Headers')
        return csv.to_dict(orient='records')

    def _bulk_insert_medicines(self, medicines):
        medicines = [Medicine(**m) for m in medicines]
        
        try:
            session = PostgresSession()
            session.bulk_save_objects(medicines)
        except IntegrityError:
            session.rollback()
            abort(422, 'Something is wrong in your CSV File')
        else:
            session.commit()
        finally:
            session.close()

    def _insert_medicines_from_csv(self, _file):
        medicines = self._read_csv(_file)
        self._bulk_insert_medicines(medicines)

    @auth_token_required(only_admin=True)
    def post(self):
        args = upload_medicine_csv.parse_args()
        _file = args.file
        self._insert_medicines_from_csv(_file)
        return {'message': 'The Medicines has been inserted'}, 201


class MedicineStockControl(Resource):

    def _get_medicine(self, medicine_id):
        session = PostgresSession()

        medicine = session.query(Medicine) \
            .filter(Medicine._id == medicine_id) \
            .one_or_none()
        
        if not medicine:
            abort(404, f'Medicine({medicine_id}) not found')
        return medicine

    def _change_stock(self, medicine_id, quantity, action):
        medicine = self._get_medicine(medicine_id)
        session = PostgresSession()
        
        if action == 'remove':
            if medicine.quantity < quantity:
                abort(412, 'Stock quantity is not enough')
            quantity *= -1

        session.query(Medicine) \
            .filter(Medicine._id == medicine_id) \
            .update({
                Medicine.quantity: medicine.quantity + quantity
            })
        session.commit()
        return medicine

    @auth_token_required()
    def patch(self, medicine_id, action):
        args = change_medicine_stock_parser.parse_args()

        if action not in ['add', 'remove']:
            abort(400, 'Invalid action')

        if args.quantity <= 0:
            abort(400, "QUANTITY must be greater than ZERO(0)")
        
        medicine = self._change_stock(medicine_id, args.quantity, action)
        response = {
            'medicine_id': medicine_id,
            'quantity': medicine.quantity,
            'amount': medicine.amount
        }
        return _json_result(response), 200
