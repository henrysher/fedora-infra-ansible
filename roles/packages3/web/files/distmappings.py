# Global list of koji tags we care about
tags = ({'name': 'Rawhide', 'tag': 'f27'},

        {'name': 'Fedora 26', 'tag': 'f26:updates'},
        {'name': 'Fedora 26', 'tag': 'f26'},
        {'name': 'Fedora 26 Testing', 'tag': 'f26-updates-testing'},

        {'name': 'Fedora 25', 'tag': 'f25:updates'},
        {'name': 'Fedora 25', 'tag': 'f25'},
        {'name': 'Fedora 25 Testing', 'tag': 'f25-updates-testing'},

	{'name': 'Fedora 24', 'tag': 'f24:updates'},
        {'name': 'Fedora 24', 'tag': 'f24'},
        {'name': 'Fedora 24 Testing', 'tag': 'f24-updates-testing'},

        {'name': 'Fedora 23', 'tag': 'f23:updates'},
        {'name': 'Fedora 23', 'tag': 'f23'},
        {'name': 'Fedora 23 Testing', 'tag': 'f23-updates-testing'},

        {'name': 'Fedora 22', 'tag': 'f22-updates'},
        {'name': 'Fedora 22', 'tag': 'f22'},
        {'name': 'Fedora 22 Testing', 'tag': 'f22-updates-testing'},

        {'name': 'Fedora 21', 'tag': 'f21-updates'},
        {'name': 'Fedora 21', 'tag': 'f21'},
        {'name': 'Fedora 21 Testing', 'tag': 'f21-updates-testing'},

        {'name': 'EPEL 7', 'tag': 'epel7'},
        {'name': 'EPEL 7 Testing', 'tag': 'epel7-testing'},

        {'name': 'EPEL 6', 'tag': 'dist-6E-epel'},
        {'name': 'EPEL 6 Testing', 'tag': 'dist-6E-epel-testing'},

        {'name': 'EPEL 5', 'tag': 'dist-5E-epel'},
        {'name': 'EPEL 5 Testing', 'tag': 'dist-5E-epel-testing'},
       )

tags_to_name_map = {}
for t in tags:
    tags_to_name_map[t['tag']] = t['name']
