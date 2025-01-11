from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    blocked = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'approved': self.approved,
            'blocked': self.blocked
        }

class CatalogCup(db.Model):
    __tablename__ = 'catalog_stakan'
    cup_type = db.Column(db.String, primary_key=True)  # Вид стакана
    throat_diameter = db.Column(db.Float, nullable=False)  # Диаметр горла
    bottom_diameter = db.Column(db.Float, nullable=False)  # Диаметр дна
    height = db.Column(db.Float, nullable=False)  # Высота
    capacity = db.Column(db.String, nullable=False)  # Емкость
    density = db.Column(db.Float, nullable=False)  # Плотность
    width = db.Column(db.Float, nullable=False)  # Ширина
    quantity_in_report = db.Column(db.Integer, nullable=False)  # Количество в рапорте
    sleeve = db.Column(db.Float, nullable=False)  # Гильза
    tooling_number = db.Column(db.Integer, nullable=False)  # Номер оснастки
    bottom_width = db.Column(db.Float, nullable=False)  # Ширина дна
    glasses_per_sleeve = db.Column(db.Integer, nullable=False)  # Количество стаканов в рукаве
    sleeves_per_box = db.Column(db.Integer, nullable=False)  # Количество рукавов в коробке
    corrugated_box_size = db.Column(db.String, nullable=False)  # Размер гофрокороба
    stacks_per_product = db.Column(db.Integer, nullable=False)  # Количество стоп в изделии
    tape_per_box_m = db.Column(db.Float, nullable=False)  # Скотч, на 1 короб м
    boxes_per_pallet = db.Column(db.Integer, nullable=False)  # Количество коробов на паллете
    packaging_pe = db.Column(db.Float, nullable=False)  # Упаковка ПЭ
    pe_sleeve_per_item = db.Column(db.Float)  # Рукав ПЭ на 1шт
    bottom_size = db.Column(db.Float, nullable=False)  # Размер донышка
    stretch_per_pallet_m = db.Column(db.Float)  # Стрейч на 1 пал. (м)
    pe_weight = db.Column(db.Float)  # Вес ПЭ
    number_of_streams = db.Column(db.Integer)  # Количество ручьев


class CatalogCompany(db.Model):
    __tablename__ = 'catalog_company'
    company_name = db.Column(db.String, primary_key=True)  # Название компании


class OrdersRegistry(db.Model):
    __tablename__ = 'orders_registry'
    registration_date = db.Column(db.Date, nullable=True, default=db.func.current_date)  # Дата регистрации
    month = db.Column(db.String, nullable=False, default=db.func.to_char(db.func.current_date(), 'Month'))  # Месяц
    company_name = db.Column(db.String, db.ForeignKey('catalog_company.company_name'), nullable=True)  # Название компании
    production_start_date = db.Column(db.Date, nullable=True)  # Дата начала производства
    order_number = db.Column(db.String, primary_key=True)  # Номер заказа
    article = db.Column(db.String, nullable=True)  # Артикул
    planned_completion_date = db.Column(db.Date, nullable=True)  # Планируемая дата завершения
    design = db.Column(db.String, nullable=False)  # Дизайн
    status = db.Column(db.String, nullable=False)  # Статус заказа
    cup_type = db.Column(db.String, db.ForeignKey('catalog_stakan.cup_type'), nullable=False)  # Тип стакана
    order_quantity = db.Column(db.Integer, nullable=True)  # Количество


class TechCardPart1(db.Model):
    __tablename__ = 'tech_card_part1'
    order_number = db.Column(db.String, db.ForeignKey('orders_registry.order_number'), primary_key=True)  # Номер заказа
    production_start_date = db.Column(db.Date, nullable=True)  # Дата запуска заказа
    customer = db.Column(db.String, nullable=True)  # Заказчик
    circulation = db.Column(db.Integer, nullable=True)  # Тираж
    cup_article = db.Column(db.String, nullable=True)  # Артикул стакана
    design = db.Column(db.String, nullable=False)  # Дизайн
    product_type = db.Column(db.String, db.ForeignKey('catalog_stakan.cup_type'), nullable=False)  # Тип изделия
    throat_diameter = db.Column(db.Float, nullable=False)  # Диаметр горла
    bottom_diameter = db.Column(db.Float, nullable=False)  # Диаметр дна
    height = db.Column(db.Float, nullable=False)  # Высота
    capacity = db.Column(db.String, nullable=False)  # Емкость
    manufacturer = db.Column(db.String, nullable=True)  # Производитель
    name = db.Column(db.String, nullable=True)  # Наименование
    density = db.Column(db.Float, nullable=False)  # Плотность
    width = db.Column(db.Float, nullable=False)  # Ширина
    pe_layer = db.Column(db.Float, nullable=True)  # Слой PE
    meters_per_circulation = db.Column(db.Float, nullable=True)  # Метры на тираж
    kg_per_circulation = db.Column(db.Float, nullable=True)  # Кг на тираж
    rapport_impressions = db.Column(db.Float, nullable=True)  # Оттиски в тираже
    bottom_material_meters = db.Column(db.Float, nullable=True)  # Расход материала на дно (метры)
    bottom_material_kg = db.Column(db.Float, nullable=True)  # Расход материала на дно (кг)
    sleeve = db.Column(db.Float, nullable=False)  # Гильза
    tooling_number = db.Column(db.Integer, nullable=False)  # Номер оснастки
    quantity_per_rapport = db.Column(db.Float, nullable=False)  # Количество на раппорте
    bottom_width = db.Column(db.Float, nullable=False)  # Ширина дна
    glasses_per_sleeve = db.Column(db.Integer, nullable=False)  # Стаканы в рукаве
    sleeves_per_box = db.Column(db.Integer, nullable=False)  # Рукава в коробке
    corrugated_box_size = db.Column(db.String, nullable=False)  # Размер коробки


class TechCardPart2(db.Model):
    __tablename__ = 'tech_card_part2'
    order_number = db.Column(db.String(50), db.ForeignKey('tech_card_part1.order_number'), primary_key=True)
    printing_unit_number = db.Column(db.String(50), nullable=True)
    lineature_anilox = db.Column(db.String(50), nullable=True)
    shaft_number = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    viscosity = db.Column(db.String(50), nullable=True)
    consumption = db.Column(db.String(50), nullable=True)
    comments = db.Column(db.Text, nullable=True)


class TechSpecification(db.Model):
    __tablename__ = 'tech_specification'

    # Fields from orders_registry (T3)
    order_number = db.Column(db.String, db.ForeignKey('orders_registry.order_number'), primary_key=True)  # 1
    article = db.Column(db.String, nullable=True)  # 2
    design = db.Column(db.String, nullable=True)  # 3
    production_start_date = db.Column(db.Date, nullable=True)  # 4
    cup_type = db.Column(db.String, nullable=True)  # 5
    order_quantity = db.Column(db.Integer, nullable=True)  # 6

    # Field from tech_card_part2 (T5)
    color = db.Column(db.String, nullable=True)  # 7

    # Calculated from tech_card_part1 and manual input
    total_cup_weight = db.Column(db.Float, nullable=True)  # 8

    # Manual input fields
    machine = db.Column(db.String, nullable=True)  # 9
    material = db.Column(db.String, nullable=True)  # 10
    paper_density = db.Column(db.String, nullable=True)  # 11
    side_wall = db.Column(db.String, nullable=True)  # 12
    size_mm = db.Column(db.Float, nullable=True)  # 13
    total_density = db.Column(db.Float, nullable=True)  # 14
    bottom = db.Column(db.String, nullable=True)  # 15
    size_mm_82_72 = db.Column(db.Float, nullable=True)  # 16
    total_density_82_72 = db.Column(db.Float, nullable=True)  # 17
    strokes_per_min = db.Column(db.Float, nullable=True)  # 18

    # Calculated fields
    roll_width_after_print = db.Column(db.Float, nullable=True)  # 19
    side_wall_weight_per_cup = db.Column(db.Float, nullable=True)  # 20
    side_wall_cutting_weight = db.Column(db.Float, nullable=True)  # 21
    total_side_wall_weight = db.Column(db.Float, nullable=True)  # 22
    blanker_waste_norm = db.Column(db.Float, nullable=True)  # 23

    # Field from catalog_stakan (T1)
    number_of_streams = db.Column(db.Integer, nullable=True)  # 24

    # More manual input and calculated fields
    utilization_ratio = db.Column(db.Float, nullable=True)  # 25
    productivity_per_hour = db.Column(db.Float, nullable=True)  # 26
    blank_consumption_per_1000 = db.Column(db.String, nullable=True)  # 27
    side_wall_blanks = db.Column(db.Float, nullable=True)  # 28
    bottom_weight = db.Column(db.Float, nullable=True)  # 29
    bottom_cutting_weight = db.Column(db.Float, nullable=True)  # 30

    # More fields from catalog_stakan (T1)
    pe_packaging = db.Column(db.Float, nullable=True)  # 31
    pe_weight = db.Column(db.Float, nullable=True)  # 32

    # Remaining calculated and automatic fields
    pe_packaging_consumption = db.Column(db.Float, nullable=True)  # 33
    stacks_per_box = db.Column(db.Integer, nullable=True)  # 34
    items_per_stack = db.Column(db.Integer, nullable=True)  # 35
    items_per_box = db.Column(db.Integer, nullable=True)  # 36
    box_dimensions = db.Column(db.String, nullable=True)  # 37
    box_label_qty = db.Column(db.Float, nullable=True)  # 38
    tape_consumption = db.Column(db.Float, nullable=True)  # 39
    tape_per_box = db.Column(db.Float, nullable=True)  # 40
    boxes_per_pallet = db.Column(db.Integer, nullable=True)  # 41
    items_per_pallet = db.Column(db.Integer, nullable=True)  # 42
    stretch_film_consumption = db.Column(db.Float, nullable=True)  # 43
    pallet_label_qty = db.Column(db.Float, nullable=True)  # 44

    def __repr__(self):
        return f'<TechSpecification {self.order_number}>'

    # Relationship with orders registry
    order = db.relationship('OrdersRegistry', backref='tech_specification')