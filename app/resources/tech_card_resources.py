from flask import make_response
from flask_restful import Resource, reqparse
from app.models import TechCardPart1, TechCardPart2
from app import db
from sqlalchemy import cast, String, text


class TechCardResource(Resource):
    def options(self, order_number=None):  # Handle both parameterized and non-parameterized routes
        response = make_response('', 204)
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, username'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    def get(self):
        # Join `TechCardPart1` and `TechCardPart2` on `order_number` and fetch all columns
        query = db.session.query(
            TechCardPart1.production_start_date.label('production_start_date'),
            TechCardPart1.customer.label('customer'),
            TechCardPart1.order_number.label('order_number'),
            TechCardPart1.circulation.label('circulation'),
            TechCardPart1.cup_article.label('cup_article'),
            TechCardPart1.design.label('design'),
            TechCardPart1.product_type.label('product_type'),
            TechCardPart1.throat_diameter.label('throat_diameter'),
            TechCardPart1.bottom_diameter.label('bottom_diameter'),
            TechCardPart1.height.label('height'),
            TechCardPart1.capacity.label('capacity'),
            TechCardPart1.manufacturer.label('manufacturer'),
            TechCardPart1.name.label('name'),
            TechCardPart1.density.label('density'),
            TechCardPart1.width.label('width'),
            TechCardPart1.pe_layer.label('pe_layer'),
            TechCardPart1.meters_per_circulation.label('meters_per_circulation'),
            TechCardPart1.kg_per_circulation.label('kg_per_circulation'),
            TechCardPart1.rapport_impressions.label('rapport_impressions'),
            TechCardPart1.bottom_material_meters.label('bottom_material_meters'),
            TechCardPart1.bottom_material_kg.label('bottom_material_kg'),
            TechCardPart1.sleeve.label('sleeve'),
            TechCardPart1.tooling_number.label('tooling_number'),
            TechCardPart1.quantity_per_rapport.label('quantity_per_rapport'),
            TechCardPart1.bottom_width.label('bottom_width'),
            TechCardPart1.glasses_per_sleeve.label('glasses_per_sleeve'),
            TechCardPart1.sleeves_per_box.label('sleeves_per_box'),
            TechCardPart1.corrugated_box_size.label('corrugated_box_size'),
            cast(TechCardPart2.printing_unit_number, String).label('printing_unit_number'),
            cast(TechCardPart2.lineature_anilox, String).label('lineature_anilox'),
            cast(TechCardPart2.shaft_number, String).label('shaft_number'),
            cast(TechCardPart2.name, String).label('part2_name'),
            cast(TechCardPart2.color, String).label('color'),
            cast(TechCardPart2.viscosity, String).label('viscosity'),
            cast(TechCardPart2.consumption, String).label('consumption'),
            cast(TechCardPart2.comments, String).label('comments')
        ).outerjoin(TechCardPart2, TechCardPart1.order_number == TechCardPart2.order_number)

        result = [row._asdict() for row in query]
        return result, 200

    def put(self, order_number):
        parser = reqparse.RequestParser()

        # Only add the fields that were modified
        parser.add_argument('manufacturer', type=str, store_missing=False)
        parser.add_argument('name', type=str, store_missing=False)
        parser.add_argument('pe_layer', type=float, store_missing=False)
        parser.add_argument('printing_unit_number', type=str, store_missing=False)
        parser.add_argument('lineature_anilox', type=str, store_missing=False)
        parser.add_argument('shaft_number', type=str, store_missing=False)
        parser.add_argument('color', type=str, store_missing=False)
        parser.add_argument('viscosity', type=str, store_missing=False)
        parser.add_argument('consumption', type=str, store_missing=False)
        parser.add_argument('comments', type=str, store_missing=False)
        parser.add_argument('part2_name', type=str, store_missing=False)

        try:
            data = parser.parse_args()

            # Split the data into part1 and part2 updates
            part1_fields = ['manufacturer', 'name', 'pe_layer']
            part2_fields = ['printing_unit_number', 'lineature_anilox', 'shaft_number',
                            'color', 'viscosity', 'consumption', 'comments', 'part2_name']

            # Only include fields that were actually sent
            part1_data = {k: v for k, v in data.items() if k in part1_fields and v is not None}
            part2_data = {k: v for k, v in data.items() if k in part2_fields and v is not None}

            if part2_data:
                # Map part2_name to name in the query if present
                if 'part2_name' in part2_data:
                    part2_data['name'] = part2_data.pop('part2_name')

                # Build dynamic SET clause based on provided fields
                set_clauses = []
                params = {'order_number': order_number}

                for key, value in part2_data.items():
                    set_clauses.append(f"{key} = :{key}")
                    params[key] = value

                sql = text(f"""
                    UPDATE tech_card_part2 
                    SET {', '.join(set_clauses)}
                    WHERE order_number = :order_number
                """)

                db.session.execute(sql, params)

            if part1_data:
                # Build dynamic SET clause for part1
                set_clauses = []
                params = {'order_number': order_number}

                for key, value in part1_data.items():
                    set_clauses.append(f"{key} = :{key}")
                    params[key] = value

                sql = text(f"""
                    UPDATE tech_card_part1 
                    SET {', '.join(set_clauses)}
                    WHERE order_number = :order_number
                """)

                db.session.execute(sql, params)

            db.session.commit()
            return {"message": "TechCard updated successfully"}, 200

        except Exception as e:
            db.session.rollback()
            import traceback
            error_details = traceback.format_exc()
            print(f"Error updating TechCard: {error_details}")
            return {
                "message": "Error updating TechCard",
                "error": str(e),
                "details": error_details
            }, 500

    def delete(self, order_number):
        try:
            # Delete records from `TechCardPart2` first (child table)
            part2 = TechCardPart2.query.filter_by(order_number=order_number).first()
            if part2:
                db.session.delete(part2)
                db.session.commit()

            # Then delete from `TechCardPart1` (parent table)
            part1 = TechCardPart1.query.filter_by(order_number=order_number).first()
            if part1:
                db.session.delete(part1)
                db.session.commit()

            return {"message": "TechCard deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error deleting TechCard: {str(e)}"}, 500