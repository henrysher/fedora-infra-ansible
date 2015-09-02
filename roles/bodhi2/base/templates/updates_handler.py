config = dict(
    # Note, the masher runs on bodhi-backend01, but this
    # runs on bodhi-backend02 (separation of concerns).
    {% if inventory_hostname.startswith('bodhi-backend02') %}
    updates_handler=True,
    {% else %}
    updates_handler=False,
    {% endif %}
)
