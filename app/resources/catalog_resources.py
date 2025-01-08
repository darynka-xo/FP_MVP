from flask_restful import Resource, reqparse
from app.models import CatalogCup
from app import db

class CatalogResource(Resource):
    def get(self, catalog_id=None):
        if catalog_id:
            cup = CatalogCup.query.get(catalog_id)
            if not cup:
                return {'message': 'Cup not found'}, 404
            return {
                'id': cup.id,
                'type': cup.type,
                'rim_diameter': cup.rim_diameter,
                'bottom_diameter': cup.bottom_diameter,
                'height': cup.height
            }, 200

        cups = CatalogCup.query.all()
        return [{'id': cup.id, 'type': cup.type} for cup in cups], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', required=True)
        parser.add_argument('rim_diameter', type=float)
        parser.add_argument('bottom_diameter', type=float)
        parser.add_argument('height', type=float)
        parser.add_argument('capacity', type=float)
        data = parser.parse_args()

        new_cup = CatalogCup(**data)
        db.session.add(new_cup)
        db.session.commit()
        return {'message': 'Cup added', 'id': new_cup.id}, 201

    def delete(self, catalog_id):
        cup = CatalogCup.query.get(catalog_id)
        if not cup:
            return {'message': 'Cup not found'}, 404
        db.session.delete(cup)
        db.session.commit()
        return {'message': 'Cup deleted'}, 200

    def put(self, catalog_id):
        cup = CatalogCup.query.get(catalog_id)
        if not cup:
            return {'message': 'Cup not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('type', required=True)
        parser.add_argument('rim_diameter', type=float)
        parser.add_argument('bottom_diameter', type=float)
        parser.add_argument('height', type=float)
        parser.add_argument('capacity', type=float)
        data = parser.parse_args()

        for key, value in data.items():
            setattr(cup, key, value)

        db.session.commit()
        return {'message': 'Cup updated'}, 200