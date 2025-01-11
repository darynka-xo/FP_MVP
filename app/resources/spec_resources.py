# spec_resources.py
from flask import make_response
from flask_restful import Resource, reqparse
from app.models import TechSpecification
from app import db
from sqlalchemy import cast, String, text


class TechSpecificationResource(Resource):
    def options(self, order_number=None):
        response = make_response('', 204)
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, username'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    def get(self):
        query = db.session.query(TechSpecification)
        result = [{
            'order_number': spec.order_number,  # 1
            'article': spec.article,  # 2
            'design': spec.design,  # 3
            'production_start_date': spec.production_start_date,  # 4
            'cup_type': spec.cup_type,  # 5
            'order_quantity': spec.order_quantity,  # 6
            'color': spec.color,  # 7
            'total_cup_weight': spec.total_cup_weight,  # 8
            'machine': spec.machine,  # 9
            'material': spec.material,  # 10
            'paper_density': spec.paper_density,  # 11
            'side_wall': spec.side_wall,  # 12
            'size_mm': spec.size_mm,  # 13
            'total_density': spec.total_density,  # 14
            'bottom': spec.bottom,  # 15
            'size_mm_82_72': spec.size_mm_82_72,  # 16
            'total_density_82_72': spec.total_density_82_72,  # 17
            'strokes_per_min': spec.strokes_per_min,  # 18
            'roll_width_after_print': spec.roll_width_after_print,  # 19
            'side_wall_weight_per_cup': spec.side_wall_weight_per_cup,  # 20
            'side_wall_cutting_weight': spec.side_wall_cutting_weight,  # 21
            'total_side_wall_weight': spec.total_side_wall_weight,  # 22
            'blanker_waste_norm': spec.blanker_waste_norm,  # 23
            'number_of_streams': spec.number_of_streams,  # 24
            'utilization_ratio': spec.utilization_ratio,  # 25
            'productivity_per_hour': spec.productivity_per_hour,  # 26
            'blank_consumption_per_1000': spec.blank_consumption_per_1000,  # 27
            'side_wall_blanks': spec.side_wall_blanks,  # 28
            'bottom_weight': spec.bottom_weight,  # 29
            'bottom_cutting_weight': spec.bottom_cutting_weight,  # 30
            'pe_packaging': spec.pe_packaging,  # 31
            'pe_weight': spec.pe_weight,  # 32
            'pe_packaging_consumption': spec.pe_packaging_consumption,  # 33
            'stacks_per_box': spec.stacks_per_box,  # 34
            'items_per_stack': spec.items_per_stack,  # 35
            'items_per_box': spec.items_per_box,  # 36
            'box_dimensions': spec.box_dimensions,  # 37
            'box_label_qty': spec.box_label_qty,  # 38
            'tape_consumption': spec.tape_consumption,  # 39
            'tape_per_box': spec.tape_per_box,  # 40
            'boxes_per_pallet': spec.boxes_per_pallet,  # 41
            'items_per_pallet': spec.items_per_pallet,  # 42
            'stretch_film_consumption': spec.stretch_film_consumption,  # 43
            'pallet_label_qty': spec.pallet_label_qty  # 44
        } for spec in query]
        return result, 200

    def put(self, order_number):
        parser = reqparse.RequestParser()

        # Add all editable fields
        editable_fields = [
            'machine', 'material', 'paper_manufacturer', 'paper_density',
            'side_wall', 'size_mm', 'total_density', 'bottom',
            'size_mm_82_72', 'total_density_82_72', 'blanker',
            'strokes_per_min', 'paper_consumption_kg_per_1000',
            'side_wall_weight_per_cup', 'side_wall_cutting_weight',
            'blanker_waste_norm', 'utilization_ratio', 'forming',
            'blank_consumption_per_1000', 'paper_consumption',
            'bottom_weight', 'bottom_cutting_weight'
        ]

        for field in editable_fields:
            parser.add_argument(field, store_missing=False)

        try:
            data = parser.parse_args()

            # Build dynamic SET clause based on provided fields
            set_clauses = []
            params = {'order_number': order_number}

            for key, value in data.items():
                if value is not None:
                    set_clauses.append(f"{key} = :{key}")
                    params[key] = value

            if set_clauses:
                sql = text(f"""
                    UPDATE tech_specification 
                    SET {', '.join(set_clauses)}
                    WHERE order_number = :order_number
                """)

                db.session.execute(sql, params)
                db.session.commit()

            return {"message": "Tech Specification updated successfully"}, 200

        except Exception as e:
            db.session.rollback()
            import traceback
            error_details = traceback.format_exc()
            print(f"Error updating Tech Specification: {error_details}")
            return {
                "message": "Error updating Tech Specification",
                "error": str(e),
                "details": error_details
            }, 500

    def delete(self, order_number):
        try:
            spec = TechSpecification.query.get(order_number)
            if spec:
                db.session.delete(spec)
                db.session.commit()
                return {"message": "Tech Specification deleted successfully"}, 200
            return {"message": "Tech Specification not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error deleting Tech Specification: {str(e)}"}, 500