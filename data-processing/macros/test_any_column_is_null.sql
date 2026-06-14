{% test any_column_is_null(model) %}

    {% set columns = dbt_utils.get_filtered_columns_in_relation(from=model) %}

    SELECT * FROM {{ model }}
    WHERE 
        {% for column in columns %}
            "{{ column }}" IS NULL
            {% if not loop.last %} OR {% endif %}
        {% endfor %}

{% endtest %}