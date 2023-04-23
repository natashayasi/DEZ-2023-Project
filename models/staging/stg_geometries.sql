{{ config(materialized='view') }}

SELECT 
    apartment_id,
    area_id,	
    building_id,
    entity_subtype,
    entity_type,
    floor_id,
    geometry,
    site_id,
    unit_id
FROM {{ source('staging','geometries') }}
