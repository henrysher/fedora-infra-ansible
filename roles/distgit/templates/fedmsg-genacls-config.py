config = {
    'genacls.consumer.enabled': True,
    'genacls.consumer.delay': 5, # 5 seconds

    # New world
    'gitoliteprefix.consumer.enabled': True,
    'gitoliteprefix.consumer.delay': 5, # 5 seconds
    'gitoliteprefix.consumer.filename': '/var/tmp/gitolite-prefix.txt',
    'gitoliteprefix.consumer.fasurl': 'https://admin.fedoraproject.org/accounts',
    'gitoliteprefix.consumer.username': "fasreadonly",
    'gitoliteprefix.consumer.password': '{{ fasReadOnlyPassword }}',
}
