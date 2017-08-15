# Global list of koji tags we care about
tags = ({'name': 'Rawhide', 'tag': 'f28'},

        {'name': 'Fedora 27', 'tag': 'f27-updates'},
        {'name': 'Fedora 27', 'tag': 'f27'},
        {'name': 'Fedora 27 Testing', 'tag': 'f27-updates-testing'},

        {'name': 'Fedora 26', 'tag': 'f26-updates'},
        {'name': 'Fedora 26', 'tag': 'f26'},
        {'name': 'Fedora 26 Testing', 'tag': 'f26-updates-testing'},

        {'name': 'Fedora 25', 'tag': 'f25:updates'},
        {'name': 'Fedora 25', 'tag': 'f25'},
        {'name': 'Fedora 25 Testing', 'tag': 'f25-updates-testing'},

        {'name': 'EPEL 7', 'tag': 'epel7'},
        {'name': 'EPEL 7 Testing', 'tag': 'epel7-testing'},

        {'name': 'EPEL 6', 'tag': 'dist-6E-epel'},
        {'name': 'EPEL 6 Testing', 'tag': 'dist-6E-epel-testing'},

       )

tags_to_name_map = {}
for t in tags:
    tags_to_name_map[t['tag']] = t['name']
