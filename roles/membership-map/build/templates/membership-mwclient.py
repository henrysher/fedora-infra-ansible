s script is for generating output for
https://fedoraproject.org/wiki/Ambassadors/MembershipService/Verification.'''
#
# Copyright (C) 2010, Susmit Shannigrahi, Susmit AT fedoraproject DOT org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import getpass
from fedora.client.fas2 import AccountSystem
import datetime
import GeoIP
from django.utils.encoding import smart_str
import mwclient

#from maxmind array
#changes are: 'RS': 'EU', 'ME': 'EU', 'AU': 'AS', 'NZ': 'AS'
#https://fedorahosted.org/fedora-infrastructure/ticket/2921
#changes are: 'IL': 'EU', 'KG': 'EU', 'LB': 'EU', 'SA': 'EU', 'AE': 'EU'


CONTINENT_MAP = {'AP': 'AS', 'EU': 'EU', 'AD': 'EU', 'AE': 'EU', 'AF': 'AS', \
 'AG': 'SA', 'AI': 'SA', 'AL': 'EU', 'AM': 'AS', 'AN': 'SA', 'AO': 'EU', \
'AQ': 'AN', 'AR': 'SA', 'AS': 'OC', 'AT': 'EU', 'AU': 'OC', 'AW': 'SA', \
'AX': 'EU', 'AZ': 'AS', 'BA': 'EU', 'BB': 'SA', 'BD': 'AS', 'BE': 'EU', \
'BF': 'EU', 'BG': 'EU', 'BH': 'AS', 'BI': 'EU', 'BJ': 'EU', 'BM': 'SA', \
'BN': 'AS', 'BO': 'SA', 'BR': 'SA', 'BS': 'SA', 'BT': 'AS', 'BV': 'EU', \
'BW': 'EU', 'BY': 'EU', 'BZ': 'SA', 'CA': 'NA', 'CC': 'AS', 'CD': 'EU', \
'CF': 'EU', 'CG': 'EU', 'CH': 'EU', 'CI': 'EU', 'CK': 'OC', 'CL': 'SA', \
'CM': 'EU', 'CN': 'AS', 'CO': 'SA', 'CR': 'SA', 'CU': 'SA', 'CV': 'EU', \
'CX': 'AS', 'CY': 'AS', 'CZ': 'EU', 'DE': 'EU', 'DJ': 'EU', 'DK': 'EU', \
'DM': 'SA', 'DO': 'SA', 'DZ': 'EU', 'EC': 'SA', 'EE': 'EU', 'EG': 'EU', \
'EH': 'EU', 'ER': 'EU', 'ES': 'EU', 'ET': 'EU', 'FI': 'EU', 'FJ': 'OC', \
'FK': 'SA', 'FM': 'OC', 'FO': 'EU', 'FR': 'EU', 'FX': 'EU', 'GA': 'EU', \
'GB': 'EU', 'GD': 'SA', 'GE': 'AS', 'GF': 'SA', 'GG': 'EU', 'GH': 'EU', \
'GI': 'EU', 'GL': 'SA', 'GM': 'EU', 'GN': 'EU', 'GP': 'SA', 'GQ': 'EU', \
'GR': 'EU', 'GS': 'SA', 'GT': 'SA', 'GU': 'OC', 'GW': 'EU', 'GY': 'SA', \
'HK': 'AS', 'HM': 'EU', 'HN': 'SA', 'HR': 'EU', 'HT': 'SA', 'HU': 'EU', \
'ID': 'AS', 'IE': 'EU', 'IL': 'EU', 'IM': 'EU', 'IN': 'AS', 'IO': 'AS', \
'IQ': 'AS', 'IR': 'AS', 'IS': 'EU', 'IT': 'EU', 'JE': 'EU', 'JM': 'SA', \
'JO': 'AS', 'JP': 'AS', 'KE': 'EU', 'KG': 'EU', 'KH': 'AS', 'KI': 'OC', \
'KM': 'EU', 'KN': 'SA', 'KP': 'AS', 'KR': 'AS', 'KW': 'AS', 'KY': 'SA', \
'KZ': 'AS', 'LA': 'AS', 'LB': 'EU', 'LC': 'SA', 'LI': 'EU', 'LK': 'AS', \
'LR': 'EU', 'LS': 'EU', 'LT': 'EU', 'LU': 'EU', 'LV': 'EU', 'LY': 'EU', \
'MA': 'EU', 'MC': 'EU', 'MD': 'EU', 'MG': 'EU', 'MH': 'OC', 'MK': 'EU', \
'ML': 'EU', 'MM': 'AS', 'MN': 'AS', 'MO': 'AS', 'MP': 'OC', 'MQ': 'SA', \
'MR': 'EU', 'MS': 'SA', 'MT': 'EU', 'MU': 'EU', 'MV': 'AS', 'MW': 'EU', \
'MX': 'NA', 'MY': 'AS', 'MZ': 'EU', 'NA': 'EU', 'NC': 'OC', 'NE': 'EU', \
'NF': 'OC', 'NG': 'EU', 'NI': 'SA', 'NL': 'EU', 'NO': 'EU', 'NP': 'AS', \
'NR': 'OC', 'NU': 'OC', 'NZ': 'AS', 'OM': 'AS', 'PA': 'SA', 'PE': 'SA', \
'PF': 'OC', 'PG': 'OC', 'PH': 'AS', 'PK': 'AS', 'PL': 'EU', 'PM': 'SA', \
'PN': 'OC', 'PR': 'SA', 'PS': 'AS', 'PT': 'EU', 'PW': 'OC', 'PY': 'SA', \
'QA': 'AS', 'RE': 'EU', 'RO': 'EU', 'RU': 'EU', 'RW': 'EU', 'SA': 'AS', \
'SB': 'OC', 'SC': 'EU', 'SD': 'EU', 'SE': 'EU', 'SG': 'AS', 'SH': 'EU', \
'SI': 'EU', 'SJ': 'EU', 'SK': 'EU', 'SL': 'EU', 'SM': 'EU', 'SN': 'EU', \
'SO': 'EU', 'SR': 'SA', 'ST': 'EU', 'SV': 'SA', 'SY': 'AS', 'SZ': 'EU', \
'TC': 'SA', 'TD': 'EU', 'TF': 'EU', 'TG': 'EU', 'TH': 'AS', 'TJ': 'AS', \
'TK': 'OC', 'TM': 'AS', 'TN': 'EU', 'TO': 'OC', 'TP': 'AS', 'TR': 'EU', \
'TT': 'SA', 'TV': 'OC', 'TW': 'AS', 'TZ': 'EU', 'UA': 'EU', 'UG': 'EU', \
'UM': 'OC', 'US': 'NA', 'UY': 'SA', 'UZ': 'AS', 'VA': 'EU', 'VC': 'SA', \
'VE': 'SA', 'VG': 'SA', 'VI': 'SA', 'VN': 'AS', 'VU': 'OC', 'WF': 'OC', \
'WS': 'OC', 'YE': 'AS', 'YT': 'EU', 'YU': 'EU', 'ZA': 'EU', 'ZM': 'EU', \
'ZR': 'EU', 'ZW': 'EU', 'RS': 'EU', 'ME': 'EU', 'AU': 'AS'}

def calc_list():
    '''Calculate the contributors list categorised by country'''
    output = []
    people_list = []
    country_list = []
    flag = 0
    final_output_list_as = []
    final_output_list_eu = []
    final_output_list_na = []
    final_output_list_latam = []
    final_output_list_unknown = []
    full_name = {'AS' : 'APAC', 'NA' : 'North America', \
'SA' : 'LATAM', 'EU' : 'EMEA', 'Unknown' : 'Unknown'}


    group_name = 'ambassadors'
#    username = 'fedoradummy'
#    password = '<%= fedoraDummyUserPassword %>'
    username = raw_input('Username: ').strip()
    password = getpass.getpass('Password: ')
    fas = AccountSystem(username=username, password=password)

    # Call fedoraproject API with mwclient
    site = mwclient.Site(('https', 'fedoraproject.org'), path='/w/')
    site.login(username, password) # Optional
    # Specify which page to edit
    page = site.Pages['Ambassadors/MembershipService/Verification2']

    #delete all the erswhile contents.
    page.edit()
    blank_page = "updating..."
    page.save(blank_page)

    print 'This takes loooooong time to execute...'

    #get all data from a group
    group_people = fas.group_members(group_name)
    #make a list of usernames of a group
    for item in group_people:
        people_list.append(item['username'])

    # get the country list from GeoIP
    countries = dict(GeoIP.country_names.items())

    # Get a dictinary of all people in FAS
    data = fas.people_by_key(key='id', search=u'*', \
fields=['human_name', 'username', 'email', 'status', 'country_code'])

    for person in people_list:
#        break
        for item in data.values():
            user_name = item['username']
            human_name = item['human_name']
            country_code = item['country_code']
            status = item['status']
            email = item['username'] + '@fedoraproject.org'



            if person == user_name:
            #print 'match'
                if status == 'active': #filter out all inactive accounts
                    if country_code is None or country_code == 'O1' \
or country_code == '  ':
                        continent_code = 'Unknown'
                    else:
                        continent_code = CONTINENT_MAP[country_code]

                   #different values for blank or non-blank fields are
                   #_____________________________________________________#
                   # Country Code  || Human Name || Number of tickets||  #
                   #_____________________________________________________#
                   # None          || None/Name  ||  0/n                 #
                   # '   '         || None/Name  ||                      #
                   # 'IN','FR' etc.|| None/Name  ||                      #
                   #_____________________________________________________#

                    if country_code is None:
                        if human_name is None:
                            flag = 1
                        else:
                            flag = 2
                    elif country_code == '  ':
                        if human_name is None:
                            flag = 1
                        else:
                            flag = 2

                    else: #if there is a country code available
                        country = countries[country_code]
                        if human_name is None:
                            flag = 3
                        else:
                            flag = 4
                    #check flag to decide o/p
                    if flag == 1:
                        entry = [user_name, user_name, 'Unknown', email, \
'Unknown']
                        output.append(entry)
                    elif flag == 2:
                        entry = [user_name, human_name, 'Unknown', email, \
'Unknown']
                        output.append(entry)
                    elif flag == 3:
                        entry = [user_name, user_name, country, email, \
continent_code]
                        output.append(entry)
                    else:
                        entry = [user_name, human_name, country, email, \
continent_code]
                        output.append(entry)

# Now we have a output list like
#[['rdsharma4u', 'Ravi Datta Sharma','India','rdsharma4u@gmail.com','1','AS'],
#['red', 'Sandro Mathys', 'Switzerland', 'sm@sandro-mathys.ch', '10', 'EU']]



    for item in output:
        #break
        continent_code = item[4]
        if continent_code == 'AS' or continent_code == 'AU':
            final_output_list_as.append(item)
        elif continent_code == 'NA':
            final_output_list_na.append(item)
        elif continent_code == 'SA':
            final_output_list_latam.append(item)
        elif continent_code == 'EU':
            final_output_list_eu.append(item)
        elif continent_code == 'Unknown':
            final_output_list_unknown.append(item)
   # sort the list according to countries
    final_string = ''
    for final_output_list in [final_output_list_as, \
final_output_list_na, final_output_list_latam, final_output_list_eu, \
final_output_list_unknown]:
        country_list = []
        #print final_output_list

        # print the full continent name from entry zero of list
        try:
            continent_code = final_output_list[0][4]

            full_cont_name = full_name[continent_code]

            full_cont_name = "<h3> %s (%s) </h3>" \
% (full_cont_name, len(final_output_list))

            final_string = final_string + full_cont_name
            #print final_string
            for item in final_output_list:

                #print item

                country = item[2]
                if country_list.count(country) == 0:
                    country_list.append(country)
                country_list.sort()

        except IndexError:
            pass
        #print country_list
        final_output_country_list = \
[[]*len(country_list) for i in range(len(country_list))]
        for item in final_output_list:
            # find the index of this entry (country) from county_list
            index = country_list.index(item[2])
            final_output_country_list[index].append(item)
        #print final_output_country_list




        #final_string = ''

        for item in final_output_country_list:
            #reverse mapping to print the country
            pos = final_output_country_list.index(item)
            num = len(item) #number of ambassador in a country.

            cnt_lst = "<h4> %s (%s) </h4>" % (country_list[pos], num)
            # add country and table formatting to string.
            final_string = final_string + cnt_lst + '<table><th style="color: white; background-color: #3074c2; font-weight: bold" align="justified">Index</th><th style="color: white; background-color: #3074c2; font-weight: bold" align="justified">Name</th><th style="color: white; background-color: #3074c2; font-weight: bold" align="justified">Email</th>'

            index = 0
            for entries in item:
                #print entries
                #break
                index = index + 1
                user_name = entries[0]
                human_name = entries[1]
                email = user_name + ' AT fedoraproject DOT org'

                #add detals.
                final = smart_str("<tr><td>" + str(index) +"</td><td> [[User:" + user_name + "| " + human_name + "]]" + "</td><td>" + email + "</td></tr>")

                final_string = final_string + final
            final_string = final_string + '</table>'

    time = datetime.datetime.utcnow()
    page.edit()
    page.save(final_string, summary = time)


    note = "{{admon/note | Last Updated : %s UTC. %s active contributors \
listed here against %s total.}}" % (time, len(output), len(people_list))
    page = site.Pages['Ambassadors/MembershipService/VerificationStats']
    page.edit()
    page.save(note, summary = time)

if __name__ == "__main__":
    calc_list()
