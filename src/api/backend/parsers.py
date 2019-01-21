from flask_restful import reqparse

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username', type=str, required=True)
create_user_parser.add_argument('password', type=str, required=True)
create_user_parser.add_argument('is_admin', type=bool, required=True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

create_provider_parser = reqparse.RequestParser()
create_provider_parser.add_argument('name', type=str, required=True)
create_provider_parser.add_argument('telephone', type=str, required=True)

create_medicine_parser = reqparse.RequestParser()
create_medicine_parser.add_argument('name', type=str, required=True)
create_medicine_parser.add_argument('medicine_type_id', type=int, required=True)
create_medicine_parser.add_argument('dosage', type=int, required=True)
create_medicine_parser.add_argument('amount', type=float, required=True)
create_medicine_parser.add_argument('quantity', type=int, default=0)
create_medicine_parser.add_argument('provider_id', type=int, required=True)
