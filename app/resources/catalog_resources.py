from flask_restful import Resource, reqparse
from app.models import CatalogCup, CatalogCompany
from app import db


class CatalogCupListResource(Resource):
    def get(self):
        try:
            cups = CatalogCup.query.all()
            cups_data = [{
                'cup_type': cup.cup_type,
                'throat_diameter': float(cup.throat_diameter) if cup.throat_diameter else None,
                'bottom_diameter': float(cup.bottom_diameter) if cup.bottom_diameter else None,
                'height': float(cup.height) if cup.height else None,
                'capacity': cup.capacity,
                'density': float(cup.density) if cup.density else None,
                'width': float(cup.width) if cup.width else None,
                'quantity_in_report': cup.quantity_in_report,
                'sleeve': float(cup.sleeve) if cup.sleeve else None,
                'tooling_number': cup.tooling_number,
                'bottom_width': float(cup.bottom_width) if cup.bottom_width else None,
                'glasses_per_sleeve': cup.glasses_per_sleeve,
                'sleeves_per_box': cup.sleeves_per_box,
                'corrugated_box_size': cup.corrugated_box_size,
                'stacks_per_product': cup.stacks_per_product,
                'tape_per_box_m': float(cup.tape_per_box_m) if cup.tape_per_box_m else None,
                'boxes_per_pallet': cup.boxes_per_pallet,
                'packaging_pe': float(cup.packaging_pe) if cup.packaging_pe else None,
                'pe_sleeve_per_item': float(cup.pe_sleeve_per_item) if cup.pe_sleeve_per_item else None,
                'bottom_size': float(cup.bottom_size) if cup.bottom_size else None,
                'stretch_per_pallet_m': float(cup.stretch_per_pallet_m) if cup.stretch_per_pallet_m else None,
                'pe_weight': float(cup.pe_weight) if cup.pe_weight else None,
                'number_of_streams': cup.number_of_streams
            } for cup in cups]
            return cups_data, 200
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500

    def post(self):
        parser = reqparse.RequestParser()
        for field in [
            'cup_type', 'throat_diameter', 'bottom_diameter', 'height',
            'capacity', 'density', 'width', 'quantity_in_report',
            'sleeve', 'tooling_number', 'bottom_width', 'glasses_per_sleeve',
            'sleeves_per_box', 'corrugated_box_size', 'stacks_per_product',
            'tape_per_box_m', 'boxes_per_pallet', 'packaging_pe',
            'pe_sleeve_per_item', 'bottom_size', 'stretch_per_pallet_m',
            'pe_weight', 'number_of_streams'
        ]:
            parser.add_argument(field)

        try:
            data = parser.parse_args()
            new_cup = CatalogCup(**data)
            db.session.add(new_cup)
            db.session.commit()
            return {'message': 'Cup added successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error adding cup: {str(e)}'}, 500


class CatalogCupDetailResource(Resource):
    def get(self, cup_type):
        try:
            cup = CatalogCup.query.get(cup_type)
            if not cup:
                return {'message': 'Cup not found'}, 404

            return {
                'cup_type': cup.cup_type,
                'throat_diameter': float(cup.throat_diameter) if cup.throat_diameter else None,
                'bottom_diameter': float(cup.bottom_diameter) if cup.bottom_diameter else None,
                'height': float(cup.height) if cup.height else None,
                'capacity': cup.capacity,
                'density': float(cup.density) if cup.density else None,
                'width': float(cup.width) if cup.width else None,
                'quantity_in_report': cup.quantity_in_report,
                'sleeve': float(cup.sleeve) if cup.sleeve else None,
                'tooling_number': cup.tooling_number,
                'bottom_width': float(cup.bottom_width) if cup.bottom_width else None,
                'glasses_per_sleeve': cup.glasses_per_sleeve,
                'sleeves_per_box': cup.sleeves_per_box,
                'corrugated_box_size': cup.corrugated_box_size,
                'stacks_per_product': cup.stacks_per_product,
                'tape_per_box_m': float(cup.tape_per_box_m) if cup.tape_per_box_m else None,
                'boxes_per_pallet': cup.boxes_per_pallet,
                'packaging_pe': float(cup.packaging_pe) if cup.packaging_pe else None,
                'pe_sleeve_per_item': float(cup.pe_sleeve_per_item) if cup.pe_sleeve_per_item else None,
                'bottom_size': float(cup.bottom_size) if cup.bottom_size else None,
                'stretch_per_pallet_m': float(cup.stretch_per_pallet_m) if cup.stretch_per_pallet_m else None,
                'pe_weight': float(cup.pe_weight) if cup.pe_weight else None,
                'number_of_streams': cup.number_of_streams
            }, 200
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500

    def delete(self, cup_type):
        try:
            cup = CatalogCup.query.get(cup_type)
            if not cup:
                return {'message': 'Cup not found'}, 404
            db.session.delete(cup)
            db.session.commit()
            return {'message': 'Cup deleted'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting cup: {str(e)}'}, 500

    def put(self, cup_type):
        try:
            cup = CatalogCup.query.get(cup_type)
            if not cup:
                return {'message': 'Cup not found'}, 404

            parser = reqparse.RequestParser()
            for field in [
                'cup_type', 'throat_diameter', 'bottom_diameter', 'height',
                'capacity', 'density', 'width', 'quantity_in_report',
                'sleeve', 'tooling_number', 'bottom_width', 'glasses_per_sleeve',
                'sleeves_per_box', 'corrugated_box_size', 'stacks_per_product',
                'tape_per_box_m', 'boxes_per_pallet', 'packaging_pe',
                'pe_sleeve_per_item', 'bottom_size', 'stretch_per_pallet_m',
                'pe_weight', 'number_of_streams'
            ]:
                parser.add_argument(field)

            data = parser.parse_args()
            for key, value in data.items():
                if value is not None:
                    setattr(cup, key, value)

            db.session.commit()
            return {'message': 'Cup updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error updating cup: {str(e)}'}, 500


class CatalogCompanyListResource(Resource):
    def get(self):
        try:
            companies = CatalogCompany.query.all()
            return [{'company_name': company.company_name} for company in companies], 200
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('company_name', required=True)

        try:
            data = parser.parse_args()
            new_company = CatalogCompany(**data)
            db.session.add(new_company)
            db.session.commit()
            return {'message': 'Company added successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error adding company: {str(e)}'}, 500


class CatalogCompanyDetailResource(Resource):
    def get(self, company_name):
        try:
            company = CatalogCompany.query.get(company_name)
            if not company:
                return {'message': 'Company not found'}, 404
            return {'company_name': company.company_name}, 200
        except Exception as e:
            return {'message': f'Server error: {str(e)}'}, 500

    def delete(self, company_name):
        try:
            company = CatalogCompany.query.get(company_name)
            if not company:
                return {'message': 'Company not found'}, 404
            db.session.delete(company)
            db.session.commit()
            return {'message': 'Company deleted'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting company: {str(e)}'}, 500

    def put(self, company_name):
        try:
            company = CatalogCompany.query.get(company_name)
            if not company:
                return {'message': 'Company not found'}, 404

            parser = reqparse.RequestParser()
            parser.add_argument('company_name', required=True)
            data = parser.parse_args()

            company.company_name = data['company_name']
            db.session.commit()
            return {'message': 'Company updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error updating company: {str(e)}'}, 500