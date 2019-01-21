from flask import abort
from flask_restful import Resource

from ..security import check_encrypted_password, generate_auth_token
from ..model import PostgresSession
from ..model.pharmacy_user import PharmacyUser
from ..parsers import login_parser


class Login(Resource):

    def _get_user(self, username):
        session = PostgresSession()

        user = session.query(
            PharmacyUser._id,
            PharmacyUser.username,
            PharmacyUser.password,
            PharmacyUser.is_admin
        ).select_from(PharmacyUser) \
        .filter(PharmacyUser.username == username) \
        .filter(PharmacyUser.is_active == True).one_or_none()

        if not user:
            abort(404, 'Usuario não encontrado')
        return user._asdict()

    def post(self):
        args = login_parser.parse_args()
        user = self._get_user(args.username)

        if check_encrypted_password(args.password, user['password']):
            return {'token': generate_auth_token(user)}
        abort(401, 'Senha Incorreta')
