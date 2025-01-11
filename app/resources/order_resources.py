from flask_restful import Resource, reqparse
from app import db
from app.models import OrdersRegistry
from datetime import datetime


class OrdersRegistryListResource(Resource):
    def get(self):
        try:
            orders = OrdersRegistry.query.all()
            return [{
                'registration_date': order.registration_date.isoformat() if order.registration_date else None,
                'month': order.month,
                'company_name': order.company_name,
                'production_start_date': order.production_start_date.isoformat() if order.production_start_date else None,
                'order_number': order.order_number,
                'article': order.article,
                'planned_completion_date': order.planned_completion_date.isoformat() if order.planned_completion_date else None,
                'design': order.design,
                'status': order.status,
                'cup_type': order.cup_type,
                'order_quantity': order.order_quantity
            } for order in orders], 200
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('registration_date')
        parser.add_argument('month')
        parser.add_argument('company_name')
        parser.add_argument('production_start_date')
        parser.add_argument('order_number', required=True)
        parser.add_argument('article')
        parser.add_argument('planned_completion_date')
        parser.add_argument('design', required=True)
        parser.add_argument('status', required=True)
        parser.add_argument('cup_type', required=True)
        parser.add_argument('order_quantity', type=int)

        try:
            data = parser.parse_args()

            # Convert date strings to Python date objects
            for date_field in ['registration_date', 'production_start_date', 'planned_completion_date']:
                if data[date_field]:
                    data[date_field] = datetime.strptime(data[date_field], '%Y-%m-%d').date()

            new_order = OrdersRegistry(**data)
            db.session.add(new_order)
            db.session.commit()
            return {'message': 'Order added successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error adding order: {str(e)}'}, 500


class OrdersRegistryDetailResource(Resource):
    def get(self, order_number):
        try:
            order = OrdersRegistry.query.get(order_number)
            if not order:
                return {'message': 'Order not found'}, 404

            return {
                'registration_date': order.registration_date.isoformat() if order.registration_date else None,
                'month': order.month,
                'company_name': order.company_name,
                'production_start_date': order.production_start_date.isoformat() if order.production_start_date else None,
                'order_number': order.order_number,
                'article': order.article,
                'planned_completion_date': order.planned_completion_date.isoformat() if order.planned_completion_date else None,
                'design': order.design,
                'status': order.status,
                'cup_type': order.cup_type,
                'order_quantity': order.order_quantity
            }, 200
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500

    def put(self, order_number):
        try:
            order = OrdersRegistry.query.get(order_number)
            if not order:
                return {'message': 'Order not found'}, 404

            parser = reqparse.RequestParser()
            parser.add_argument('registration_date')
            parser.add_argument('month')
            parser.add_argument('company_name')
            parser.add_argument('production_start_date')
            parser.add_argument('order_number')
            parser.add_argument('article')
            parser.add_argument('planned_completion_date')
            parser.add_argument('design')
            parser.add_argument('status')
            parser.add_argument('cup_type')
            parser.add_argument('order_quantity', type=int)

            data = parser.parse_args()

            # Convert date strings to Python date objects
            for date_field in ['registration_date', 'production_start_date', 'planned_completion_date']:
                if data[date_field]:
                    try:
                        data[date_field] = datetime.strptime(data[date_field], '%Y-%m-%d').date()
                    except ValueError:
                        pass  # Skip if date format is invalid

            # Update only provided fields
            for key, value in data.items():
                if value is not None:
                    setattr(order, key, value)

            db.session.commit()
            return {'message': 'Order updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error updating order: {str(e)}'}, 500

    def delete(self, order_number):
        try:
            order = OrdersRegistry.query.get(order_number)
            if not order:
                return {'message': 'Order not found'}, 404

            db.session.delete(order)
            db.session.commit()
            return {'message': 'Order deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting order: {str(e)}'}, 500