# Global list of koji tags we care about
tags = ({'name': 'Rawhide', 'tag': 'f31'},

        {'name': 'Fedora 30', 'tag': 'f30-updates'},
        {'name': 'Fedora 30', 'tag': 'f30'},
        {'name': 'Fedora 30 Testing', 'tag': 'f30-updates-testing'},

        {'name': 'Fedora 29', 'tag': 'f29-updates'},
        {'name': 'Fedora 29', 'tag': 'f29'},
        {'name': 'Fedora 29 Testing', 'tag': 'f29-updates-testing'},

        {'name': 'Fedora 28', 'tag': 'f28-updates'},
        {'name': 'Fedora 28', 'tag': 'f28'},
        {'name': 'Fedora 28 Testing', 'tag': 'f28-updates-testing'},

        {'name': 'Fedora 27', 'tag': 'f27-updates'},
        {'name': 'Fedora 27', 'tag': 'f27'},
        {'name': 'Fedora 27 Testing', 'tag': 'f27-updates-testing'},

        {'name': 'Fedora 26', 'tag': 'f26-updates'},
        {'name': 'Fedora 26', 'tag': 'f26'},
        {'name': 'Fedora 26 Testing', 'tag': 'f26-updates-testing'},

        {'name': 'Fedora 25', 'tag': 'f25:updates'},
        {'name': 'Fedora 25', 'tag': 'f25'},
        {'name': 'Fedora 25 Testing', 'tag': 'f25-updates-testing'},

        {'name': 'EPEL 8', 'tag': 'epel8'},
        {'name': 'EPEL 8 Testing', 'tag': 'epel8-testing'},
        {'name': 'EPEL 8 Staging', 'tag': 'epel8-staging'},

        {'name': 'EPEL 7', 'tag': 'epel7'},
        {'name': 'EPEL 7 Testing', 'tag': 'epel7-testing'},

        {'name': 'EPEL 6', 'tag': 'dist-6E-epel'},
        {'name': 'EPEL 6 Testing', 'tag': 'dist-6E-epel-testing'},

       )

tags_to_name_map = {}
for t in tags:
    tags_to_name_map[t['tag']] = t['name']
