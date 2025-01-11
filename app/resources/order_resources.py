from flask_restful import Resource, reqparse
from app.models import OrdersRegistry, CatalogCompany, CatalogCup
from app import db


class OrdersRegistryResource(Resource):
    def get(self):
        orders = OrdersRegistry.query.all()
        return [{
            'registration_date': order.registration_date,
            'month': order.month,
            'company_name': order.company_name,
            'production_start_date': order.production_start_date,
            'order_number': order.order_number,
            'article': order.article,
            'planned_completion_date': order.planned_completion_date,
            'design': order.design,
            'status': order.status,
            'cup_type': order.cup_type,
            'order_quantity': order.order_quantity
        } for order in orders], 200

    def put(self, order_number):
        order = OrdersRegistry.query.get(order_number)
        if not order:
            return {'message': 'Order not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('company_name')
        parser.add_argument('cup_type')
        parser.add_argument('status')
        parser.add_argument('registration_date')
        parser.add_argument('production_start_date')
        parser.add_argument('planned_completion_date')
        parser.add_argument('article')
        parser.add_argument('design')
        parser.add_argument('order_quantity', type=int)
        data = parser.parse_args()

        # Validate company_name
        if data['company_name'] and not CatalogCompany.query.filter_by(company_name=data['company_name']).first():
            return {'message': 'Invalid company_name'}, 400

        # Validate cup_type
        if data['cup_type'] and not CatalogCup.query.filter_by(cup_type=data['cup_type']).first():
            return {'message': 'Invalid cup_type'}, 400

        for key, value in data.items():
            if value is not None:
                setattr(order, key, value)

        db.session.commit()
        return {'message': 'Order updated successfully'}, 200

    def delete(self, order_number):
        order = OrdersRegistry.query.get(order_number)
        if not order:
            return {'message': 'Order not found'}, 404

        db.session.delete(order)
        db.session.commit()
        return {'message': 'Order deleted successfully'}, 200