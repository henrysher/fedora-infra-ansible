config = {
    # These are mailing lists that we don't publish to fedmsg (because spam or privacy)
    'mailman.excluded_lists': [
        'scm-commits',      # too much traffic
        'council-private',  # private list
        'cwg-private',      # private list
        'fesco',            # private list
        'security-private', # private list
        'diversity-private', # private list
    ],
}
