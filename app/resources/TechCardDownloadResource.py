from flask import send_file
from flask_restful import Resource
from io import BytesIO
from app.models import TechCardPart1, TechCardPart2
from app.services.tech_card_generator import TechCardGenerator
import os


class TechCardDownloadResource(Resource):
    def get(self, order_number):
        try:
            # Get the data
            part1 = TechCardPart1.query.get(order_number)
            part2 = TechCardPart2.query.get(order_number)

            if not part1:
                return {'message': 'Tech card not found'}, 404

            # Initialize generator with template
            template_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'templates',
                'tech_card_template.xlsx'
            )
            generator = TechCardGenerator(template_path)

            # Generate Excel
            excel_content = generator.generate_tech_card(part1, part2)

            # Create response
            excel_buffer = BytesIO(excel_content)
            excel_buffer.seek(0)

            return send_file(
                excel_buffer,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=f'tech_card_{order_number}.xlsx'
            )

        except Exception as e:
            print(f"Error generating tech card: {str(e)}")  # Added for debugging
            return {'message': f'Error generating tech card: {str(e)}'}, 500