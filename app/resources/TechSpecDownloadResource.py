from flask import send_file
from flask_restful import Resource
from io import BytesIO
from app.models import TechSpecification
from app.services.tech_spec_generator import TechSpecGenerator
import os


class TechSpecDownloadResource(Resource):
    def get(self, order_number):
        try:
            # Get the data
            spec = TechSpecification.query.get(order_number)

            if not spec:
                return {'message': 'Tech specification not found'}, 404

            # Initialize generator with template
            template_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'templates',
                'tech_spec_template.xlsx'
            )
            generator = TechSpecGenerator(template_path)

            # Generate Excel
            excel_content = generator.generate_tech_spec(spec)

            # Create response
            excel_buffer = BytesIO(excel_content)
            excel_buffer.seek(0)

            return send_file(
                excel_buffer,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=f'tech_spec_{order_number}.xlsx'
            )

        except Exception as e:
            print(f"Error generating tech spec: {str(e)}")
            return {'message': f'Error generating tech spec: {str(e)}'}, 500