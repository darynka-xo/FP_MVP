ALTER TABLE tech_card_part1
    ALTER COLUMN rapport_impressions DROP NOT NULL,
    ALTER COLUMN meters_per_circulation DROP NOT NULL,
    ALTER COLUMN kg_per_circulation DROP NOT NULL,
    ALTER COLUMN bottom_material_meters DROP NOT NULL,
    ALTER COLUMN bottom_material_kg DROP NOT NULL;

CREATE OR REPLACE FUNCTION create_tech_card_on_status_change()
RETURNS TRIGGER AS $$
DECLARE
    throat_diameter_value NUMERIC;
    bottom_diameter_value NUMERIC;
    height_value NUMERIC;
    capacity_value VARCHAR;
    density_value NUMERIC;
    width_value NUMERIC;
    sleeve_value NUMERIC;
    tooling_number_value NUMERIC;
    quantity_per_rapport NUMERIC;
    bottom_width_value NUMERIC;
    glasses_per_sleeve_value NUMERIC;
    sleeves_per_box_value NUMERIC;
    corrugated_box_size_value VARCHAR;
BEGIN
    -- Check if a tech card already exists for this order
    IF NOT EXISTS (
        SELECT 1 FROM tech_card_part1 WHERE order_number = NEW.order_number
    ) THEN
        -- Get data from catalog_stakan based on cup_type
        SELECT
            CAST(throat_diameter AS NUMERIC),
            CAST(bottom_diameter AS NUMERIC),
            CAST(height AS NUMERIC),
            capacity,
            CAST(density AS NUMERIC),
            CAST(width AS NUMERIC),
            CAST(sleeve AS NUMERIC),
            CAST(tooling_number AS NUMERIC),
            CAST(quantity_in_report AS NUMERIC),
            CAST(bottom_width AS NUMERIC),
            CAST(glasses_per_sleeve AS NUMERIC),
            CAST(sleeves_per_box AS NUMERIC),
            corrugated_box_size
        INTO
            throat_diameter_value,
            bottom_diameter_value,
            height_value,
            capacity_value,
            density_value,
            width_value,
            sleeve_value,
            tooling_number_value,
            quantity_per_rapport,
            bottom_width_value,
            glasses_per_sleeve_value,
            sleeves_per_box_value,
            corrugated_box_size_value
        FROM catalog_stakan
        WHERE cup_type = NEW.cup_type;

        -- Insert the new tech card with NULLs for calculated fields
        INSERT INTO tech_card_part1 (
            order_number,
            production_start_date,
            customer,
            circulation,
            cup_article,
            design,
            product_type,
            throat_diameter,
            bottom_diameter,
            height,
            capacity,
            density,
            width,
            sleeve,
            tooling_number,
            quantity_per_rapport,
            bottom_width,
            glasses_per_sleeve,
            sleeves_per_box,
            corrugated_box_size,
            rapport_impressions,
            meters_per_circulation,
            kg_per_circulation,
            bottom_material_meters,
            bottom_material_kg
        )
        VALUES (
            NEW.order_number,
            NEW.production_start_date,
            NEW.company_name,
            NEW.order_quantity,
            NEW.article,
            NEW.design,
            NEW.cup_type,
            throat_diameter_value,
            bottom_diameter_value,
            height_value,
            capacity_value,
            density_value,
            width_value,
            sleeve_value,
            tooling_number_value,
            quantity_per_rapport,
            bottom_width_value,
            glasses_per_sleeve_value,
            sleeves_per_box_value,
            corrugated_box_size_value,
            NULL, -- rapport_impressions
            NULL, -- meters_per_circulation
            NULL, -- kg_per_circulation
            NULL, -- bottom_material_meters
            NULL  -- bottom_material_kg
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER trigger_create_tech_card
AFTER UPDATE OF status ON orders_registry
FOR EACH ROW
WHEN (NEW.status = 'В работе' AND OLD.status IS DISTINCT FROM NEW.status)
EXECUTE FUNCTION create_tech_card_on_status_change();

CREATE OR REPLACE FUNCTION calculate_tech_card_fields()
RETURNS TRIGGER AS $$
BEGIN
    -- Perform calculations for the inserted row
    UPDATE tech_card_part1
    SET
        rapport_impressions = ROUND(circulation::NUMERIC / quantity_per_rapport, 5),
        meters_per_circulation = ROUND(((rapport_impressions * sleeve / 1000) * 1.05) + 250, 5),
        kg_per_circulation = ROUND(meters_per_circulation * (width / 1000) * (density / 1000), 5),
        bottom_material_meters = ROUND((circulation::NUMERIC * 0.084) * 1.04, 5),
        bottom_material_kg = ROUND((bottom_material_meters * 0.082) * 0.217, 5)
    WHERE order_number = NEW.order_number;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_calculate_tech_card_fields
AFTER INSERT ON tech_card_part1
FOR EACH ROW
EXECUTE FUNCTION calculate_tech_card_fields();

ALTER TABLE tech_card_part2
    ALTER COLUMN printing_unit_number DROP NOT NULL,
    ALTER COLUMN lineature_anilox DROP NOT NULL,
    ALTER COLUMN shaft_number DROP NOT NULL,
    ALTER COLUMN name DROP NOT NULL,
    ALTER COLUMN color DROP NOT NULL,
    ALTER COLUMN viscosity DROP NOT NULL,
    ALTER COLUMN consumption DROP NOT NULL,
    ALTER COLUMN comments DROP NOT NULL;

CREATE OR REPLACE FUNCTION insert_into_tech_card_part2()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert a new row into tech_card_part2 with order_number from tech_card_part1
    INSERT INTO tech_card_part2 (
        order_number, -- Номер заказа
        printing_unit_number, -- Номер печатного узла
        lineature_anilox, -- Линеатура / Емкость анилокса
        shaft_number, -- Номер вала
        name, -- Наименование
        color, -- Цвет
        viscosity, -- Вязкость, с
        consumption, -- Расход г
        comments -- Комментарии
    )
    VALUES (
        NEW.order_number, -- Automatically pulled from tech_card_part1
        NULL, -- Other fields default to NULL
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_insert_tech_card_part2
AFTER UPDATE ON tech_card_part1
FOR EACH ROW
EXECUTE FUNCTION insert_into_tech_card_part2();


-- Change the default value of the "status" column to 'Новая'
ALTER TABLE orders_registry
ALTER COLUMN status SET DEFAULT 'Новая';