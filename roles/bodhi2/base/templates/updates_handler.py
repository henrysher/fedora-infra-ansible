config = dict(
    # TODO -- we're thinking about moving this to bodhi-backend02
    {% if inventory_hostname.startswith('bodhi-backend01') %}
    updates_handler=True,
    {% else %}
    updates_handler=False,
    {% endif %}
)
