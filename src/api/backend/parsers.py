from flask_restful import reqparse

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username', type=str, required=True)
create_user_parser.add_argument('password', type=str, required=True)
create_user_parser.add_argument('is_admin', type=bool, required=True)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)
