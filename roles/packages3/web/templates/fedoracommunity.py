config = {
    {% if install_packages_indexer %}
    'fedoracommunity.fedmsg.consumer.enabled': True,
    {% else %}
    'fedoracommunity.fedmsg.consumer.enabled': False,
    {% endif %}
}
