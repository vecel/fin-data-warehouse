{% macro to_date_id(column_name) %}
    TO_CHAR({{ column_name }}, 'YYYYMMDD')::INT
{% endmacro %}