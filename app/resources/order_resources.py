from flask_restful import Resource
from app.models import OrderRegistry
from app import db

class OrderResource(Resource):
    def get(self, order_id):
        order = OrderRegistry.query.get(order_id)
        if not order:
            return {'message': 'Order not found'}, 404
        return {
            'id': order.id,
            'customer': order.customer,
            'status': order.status
        }, 200

    def delete(self, order_id):
        order = OrderRegistry.query.get(order_id)
        if not order:
            return {'message': 'Order not found'}, 404
        db.session.delete(order)
        db.session.commit()
        return {'message': 'Order deleted'}, 200

class OrderListResource(Resource):
    def get(self):
        orders = OrderRegistry.query.all()
        return [{'id': order.id, 'customer': order.customer} for order in orders], 200