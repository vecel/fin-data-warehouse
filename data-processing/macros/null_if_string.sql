{% macro null_if_on_string(source_column, target_column) %}
    NULLIF(NULLIF(TRIM({{ source_column }}::VARCHAR(50)), ''), 'null') AS {{ target_column }}
{% endmacro %}