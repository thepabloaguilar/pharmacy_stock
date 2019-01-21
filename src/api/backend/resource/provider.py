from flask import abort
from flask_restful import Resource

from ..model import PostgresSession
from ..model.provider import Provider
from ..security import auth_token_required
from ..parsers import create_provider_parser
from ..utils import _json_result

class ProviderResource(Resource):

    def _get_provider(self, provider_id):
        session = PostgresSession()

        provider = session.query(Provider) \
            .filter(Provider._id == provider_id)
        
        if not self.user_info['is_admin']:
            provider = provider.filter(Provider.is_active == True)
        provider = provider.one_or_none()
        
        if not provider:
            abort(404, 'Provider not found')
        return provider

    def _create_provider(self, informations):
        provider = Provider(
            name=informations.name,
            telephone=informations.telephone
        )

        session = PostgresSession()
        session.add(provider)
        session.commit()
        session.close()
        return provider

    def _inactive_provider(self, provider_id):
        provider = self._get_provider(provider_id)
        session = PostgresSession()

        session.query(Provider) \
        .filter(Provider._id == provider_id) \
        .update({
            Provider.is_active: not provider.is_active
        })
        session.commit()
        return provider

    @auth_token_required()
    def get(self, provider_id):
        provider = self._get_provider(provider_id)
        _provider = {
            'id': provider._id,
            'name': provider.name,
            'telephone': provider.telephone,
            'is_active': provider.is_active,
            'creation_date': provider.creation_date,
        }
        return _json_result(_provider), 200
    
    @auth_token_required(only_admin=True)
    def post(self):
        args = create_provider_parser.parse_args()
        self._create_provider(args)
        return {'message': f'Provider {args.name} was created successfuly'}, 201
    
    @auth_token_required(only_admin=True)
    def patch(self, provider_id):
        provider = self._inactive_provider(provider_id)
        action = 'activated' if provider.is_active else 'inactivated'
        return {'message': f'Provider "{provider.name}" {action}'}, 200


class ProvidersResource(Resource):
    
    def _get_providers(self):
        session = PostgresSession()
        providers = session.query(
            Provider._id.label('id'),
            Provider.name,
            Provider.telephone,
            Provider.is_active,
            Provider.creation_date
        )

        if not self.user_info['is_admin']:
            providers = providers.filter(Provider.is_active == True)
        return [p._asdict() for p in providers]

    @auth_token_required()
    def get(self):
        return _json_result(self._get_providers()), 200
