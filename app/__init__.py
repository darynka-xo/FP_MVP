from decimal import Decimal
from flask.json import JSONEncoder
from flask import Flask
from flask_cors import CORS
import json
from flask import Response
from app.extensions import db, migrate


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.json_encoder = CustomJSONEncoder

    # Initialize extensions
    db.init_app(app)

    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://localhost:3000"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "username"],
        expose_headers=["Set-Cookie"]
    )

    # Configure API
    from flask_restful import Api
    api = Api(app)
    api.representations = {
        'application/json': lambda data, code, headers: Response(
            json.dumps(data, cls=CustomJSONEncoder),
            status=code,
            content_type='application/json'
        )
    }

    # Register Resources
    from app.resources.user_resources import UserRegister, UserLogin, UserLogout
    from app.resources.tech_card_resources import TechCardResource
    from app.resources.spec_resources import TechSpecificationResource
    from app.resources.user_resources import UserApprovalList, UserApproveDeny
    from app.resources.TechCardDownloadResource import TechCardDownloadResource
    from app.resources.TechSpecDownloadResource import TechSpecDownloadResource
    from app.resources.catalog_resources import CatalogCupListResource, CatalogCupDetailResource, \
        CatalogCompanyListResource, CatalogCompanyDetailResource
    from app.resources.order_resources import OrdersRegistryListResource, OrdersRegistryDetailResource


    # Routes
    api.add_resource(UserApproveDeny, '/api/users/<int:user_id>/approve-deny')
    api.add_resource(UserApprovalList, '/api/users/unapproved')
    api.add_resource(CatalogCupListResource, '/api/catalog/cups')
    api.add_resource(CatalogCupDetailResource, '/api/catalog/cups/<string:cup_type>')
    api.add_resource(CatalogCompanyListResource, '/api/catalog/companies')
    api.add_resource(CatalogCompanyDetailResource, '/api/catalog/companies/<string:company_name>')
    api.add_resource(UserRegister, '/api/users/register')
    api.add_resource(UserLogin, '/api/users/login')
    api.add_resource(UserLogout, '/api/users/logout')
    api.add_resource(OrdersRegistryListResource, '/api/orders-registry')
    api.add_resource(OrdersRegistryDetailResource, '/api/orders-registry/<string:order_number>')
    api.add_resource(TechCardResource, '/api/tech-cards/combined', '/api/tech-cards/combined/<string:order_number>')
    api.add_resource(TechSpecificationResource, '/api/tech-specifications', '/api/tech-specifications/<string:order_number>')
    api.add_resource(TechCardDownloadResource, '/api/tech-cards/download/<string:order_number>')
    api.add_resource(TechSpecDownloadResource, '/api/tech-specifications/download/<string:order_number>')

    return app