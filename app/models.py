from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class CatalogCup(db.Model):
    __tablename__ = 'catalog_cup'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    rim_diameter = db.Column(db.Float)
    bottom_diameter = db.Column(db.Float)
    height = db.Column(db.Float)
    capacity = db.Column(db.Float)
    density = db.Column(db.Float)
    width = db.Column(db.Float)
    report_quantity = db.Column(db.Integer)
    sleeve = db.Column(db.Float)
    equipment_number = db.Column(db.String)
    bottom_width = db.Column(db.Float)
    sleeve_cups = db.Column(db.Integer)
    box_sleeves = db.Column(db.Integer)
    corrugated_box_size = db.Column(db.String)
    product_stops = db.Column(db.Integer)
    tape_per_box = db.Column(db.Float)
    pallet_boxes = db.Column(db.Integer)
    pe_packaging = db.Column(db.Float)
    pe_sleeve_per_item = db.Column(db.Float)
    bottom_size = db.Column(db.Float)
    stretch_per_pallet = db.Column(db.Float)
    pe_weight = db.Column(db.Float)
    streams = db.Column(db.Integer)

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class OrderRegistry(db.Model):
    __tablename__ = 'order_registry'
    id = db.Column(db.Integer, primary_key=True)
    registration_date = db.Column(db.Date, nullable=False)
    month = db.Column(db.String, nullable=False)
    customer = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date)
    order_number = db.Column(db.String, unique=True, nullable=False)
    article = db.Column(db.String, nullable=False)
    planned_completion_date = db.Column(db.Date)
    design = db.Column(db.String)
    status = db.Column(db.String, nullable=False)
    cup_type = db.Column(db.String, nullable=False)
    order_quantity = db.Column(db.Integer)

class TechCardPart1(db.Model):
    __tablename__ = 'tech_card_part1'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_registry.id'))
    launch_date = db.Column(db.Date)
    customer = db.Column(db.String)
    article = db.Column(db.String)
    design = db.Column(db.String)
    product_type = db.Column(db.String)
    rim_diameter = db.Column(db.Float)
    bottom_diameter = db.Column(db.Float)
    height = db.Column(db.Float)
    capacity = db.Column(db.Float)
    density = db.Column(db.Float)

class TechCardPart2(db.Model):
    __tablename__ = 'tech_card_part2'
    id = db.Column(db.Integer, primary_key=True)
    tech_card_id = db.Column(db.Integer, db.ForeignKey('tech_card_part1.id'))
    printing_unit_number = db.Column(db.String)
    lineature_capacity = db.Column(db.String)
    shaft_number = db.Column(db.String)
    color = db.Column(db.String)
    viscosity = db.Column(db.Float)
    consumption = db.Column(db.Float)
    comments = db.Column(db.Text)

class Specification(db.Model):
    __tablename__ = 'specification'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_registry.id'))
    article = db.Column(db.String)
    design = db.Column(db.String)
    launch_date = db.Column(db.Date)
    cup_type = db.Column(db.String)
    order_quantity = db.Column(db.Integer)
    color = db.Column(db.String)
    total_weight = db.Column(db.Float)
    machine = db.Column(db.String)
    material = db.Column(db.String)
    paper_density = db.Column(db.String)
    side_wall = db.Column(db.String)
    size = db.Column(db.Float)
    overall_density = db.Column(db.Float)
    bottom = db.Column(db.String)
    bottom_size = db.Column(db.Float)
    production_speed = db.Column(db.Float)