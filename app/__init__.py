from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)

    # Register Resources
    from app.resources.user_resources import UserRegister, UserLogin
    from app.resources.catalog_resources import CatalogResource
    from app.resources.order_resources import OrderResource, OrderListResource
    from app.resources.tech_card_resources import TechCardPart1Resource, TechCardPart2Resource
    from app.resources.spec_resources import SpecificationResource

    api.add_resource(UserRegister, '/api/users/register')
    api.add_resource(UserLogin, '/api/users/login')
    api.add_resource(CatalogResource, '/api/catalog/<int:catalog_id>')
    api.add_resource(OrderResource, '/api/orders/<int:order_id>')
    api.add_resource(OrderListResource, '/api/orders')
    api.add_resource(TechCardPart1Resource, '/api/tech-cards/part1/<int:card_id>')
    api.add_resource(TechCardPart2Resource, '/api/tech-cards/part2/<int:card_id>')
    api.add_resource(SpecificationResource, '/api/specifications/<int:spec_id>')

    return app