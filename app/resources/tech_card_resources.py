from flask_restful import Resource
from app.models import TechCardPart1
from app import db

class TechCardResource(Resource):
    def get(self, tech_card_id):
        tech_card = TechCardPart1.query.get(tech_card_id)
        if not tech_card:
            return {'message': 'Tech card not found'}, 404
        return {
            'id': tech_card.id,
            'cup_type': tech_card.cup_type,
            'design': tech_card.design
        }, 200

    def delete(self, tech_card_id):
        tech_card = TechCardPart1.query.get(tech_card_id)
        if not tech_card:
            return {'message': 'Tech card not found'}, 404
        db.session.delete(tech_card)
        db.session.commit()
        return {'message': 'Tech card deleted'}, 200