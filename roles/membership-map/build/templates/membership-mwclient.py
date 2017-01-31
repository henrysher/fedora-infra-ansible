#!/usr/bin/python
''' This script is for generating output for
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
from kitchen.text.converters import to_bytes
import mwclient

#from maxmind array
#changes are: 'RS': 'EU', 'ME': 'EU', 'AU': 'AS', 'NZ': 'AS'
#https://fedorahosted.org/fedora-infrastructure/ticket/2921
#changes are: 'IL': 'EU', 'KG': 'EU', 'LB': 'EU', 'SA': 'EU', 'AE': 'EU'


CONTINENT_MAP = {'AP': 'AS', 'EU': 'EU', 'AD': 'EU', 'AE': 'EU', 'AF': 'AS', \
 'AG': 'SA', 'AI': 'SA', 'AL': 'EU', 'AM': 'AS', 'AN': 'SA', 'AO': 'AF', \
'AQ': 'AN', 'AR': 'SA', 'AS': 'OC', 'AT': 'EU', 'AU': 'OC', 'AW': 'SA', \
'AX': 'EU', 'AZ': 'AS', 'BA': 'EU', 'BB': 'SA', 'BD': 'AS', 'BE': 'EU', \
'BF': 'AF', 'BG': 'EU', 'BH': 'AS', 'BI': 'AF', 'BJ': 'AF', 'BM': 'SA', \
'BN': 'AS', 'BO': 'SA', 'BR': 'SA', 'BS': 'SA', 'BT': 'AS', 'BV': 'AF', \
'BW': 'AF', 'BY': 'EU', 'BZ': 'SA', 'CA': 'NA', 'CC': 'AS', 'CD': 'AF', \
'CF': 'AF', 'CG': 'AF', 'CH': 'EU', 'CI': 'AF', 'CK': 'OC', 'CL': 'SA', \
'CM': 'AF', 'CN': 'AS', 'CO': 'SA', 'CR': 'SA', 'CU': 'SA', 'CV': 'AF', \
'CX': 'AS', 'CY': 'AS', 'CZ': 'EU', 'DE': 'EU', 'DJ': 'AF', 'DK': 'EU', \
'DM': 'SA', 'DO': 'SA', 'DZ': 'AF', 'EC': 'SA', 'EE': 'EU', 'EG': 'AF', \
'EH': 'AF', 'ER': 'AF', 'ES': 'EU', 'ET': 'AF', 'FI': 'EU', 'FJ': 'OC', \
'FK': 'SA', 'FM': 'OC', 'FO': 'EU', 'FR': 'EU', 'FX': 'EU', 'GA': 'AF', \
'GB': 'EU', 'GD': 'SA', 'GE': 'AS', 'GF': 'SA', 'GG': 'EU', 'GH': 'AF', \
'GI': 'EU', 'GL': 'SA', 'GM': 'AF', 'GN': 'AF', 'GP': 'SA', 'GQ': 'AF', \
'GR': 'EU', 'GS': 'SA', 'GT': 'SA', 'GU': 'OC', 'GW': 'AF', 'GY': 'SA', \
'HK': 'AS', 'HM': 'AF', 'HN': 'SA', 'HR': 'EU', 'HT': 'SA', 'HU': 'EU', \
'ID': 'AS', 'IE': 'EU', 'IL': 'EU', 'IM': 'EU', 'IN': 'AS', 'IO': 'AS', \
'IQ': 'AS', 'IR': 'AS', 'IS': 'EU', 'IT': 'EU', 'JE': 'EU', 'JM': 'SA', \
'JO': 'AS', 'JP': 'AS', 'KE': 'AF', 'KG': 'EU', 'KH': 'AS', 'KI': 'OC', \
'KM': 'AF', 'KN': 'SA', 'KP': 'AS', 'KR': 'AS', 'KW': 'AS', 'KY': 'SA', \
'KZ': 'AS', 'LA': 'AS', 'LB': 'EU', 'LC': 'SA', 'LI': 'EU', 'LK': 'AS', \
'LR': 'AF', 'LS': 'AF', 'LT': 'EU', 'LU': 'EU', 'LV': 'EU', 'LY': 'AF', \
'MA': 'AF', 'MC': 'EU', 'MD': 'EU', 'MG': 'AF', 'MH': 'OC', 'MK': 'EU', \
'ML': 'AF', 'MM': 'AS', 'MN': 'AS', 'MO': 'AS', 'MP': 'OC', 'MQ': 'SA', \
'MR': 'AF', 'MS': 'SA', 'MT': 'EU', 'MU': 'AF', 'MV': 'AS', 'MW': 'AF', \
'MX': 'NA', 'MY': 'AS', 'MZ': 'AF', 'NA': 'AF', 'NC': 'OC', 'NE': 'AF', \
'NF': 'OC', 'NG': 'AF', 'NI': 'SA', 'NL': 'EU', 'NO': 'EU', 'NP': 'AS', \
'NR': 'OC', 'NU': 'OC', 'NZ': 'AS', 'OM': 'AS', 'PA': 'SA', 'PE': 'SA', \
'PF': 'OC', 'PG': 'OC', 'PH': 'AS', 'PK': 'AS', 'PL': 'EU', 'PM': 'SA', \
'PN': 'OC', 'PR': 'SA', 'PS': 'AS', 'PT': 'EU', 'PW': 'OC', 'PY': 'SA', \
'QA': 'AS', 'RE': 'AF', 'RO': 'EU', 'RU': 'EU', 'RW': 'AF', 'SA': 'AS', \
'SB': 'OC', 'SC': 'AF', 'SD': 'AF', 'SE': 'EU', 'SG': 'AS', 'SH': 'AF', \
'SI': 'EU', 'SJ': 'EU', 'SK': 'EU', 'SL': 'AF', 'SM': 'EU', 'SN': 'AF', \
'SO': 'AF', 'SR': 'SA', 'ST': 'AF', 'SV': 'SA', 'SY': 'AS', 'SZ': 'AF', \
'TC': 'SA', 'TD': 'AF', 'TF': 'AF', 'TG': 'AF', 'TH': 'AS', 'TJ': 'AS', \
'TK': 'OC', 'TM': 'AS', 'TN': 'AF', 'TO': 'OC', 'TP': 'AS', 'TR': 'EU', \
'TT': 'SA', 'TV': 'OC', 'TW': 'AS', 'TZ': 'AF', 'UA': 'EU', 'UG': 'AF', \
'UM': 'OC', 'US': 'NA', 'UY': 'SA', 'UZ': 'AS', 'VA': 'EU', 'VC': 'SA', \
'VE': 'SA', 'VG': 'SA', 'VI': 'SA', 'VN': 'AS', 'VU': 'OC', 'WF': 'OC', \
'WS': 'OC', 'YE': 'AS', 'YT': 'AF', 'YU': 'EU', 'ZA': 'AF', 'ZM': 'AF', \
'ZR': 'AF', 'ZW': 'AF', 'RS': 'EU', 'ME': 'EU', 'AU': 'AS'}


def calc_list():
    '''Calculate the contributors list categorised by country'''
    output = []
    people_list = []
    country_list = []
    inactive_list = []
    flag = 0
    final_output_list_as = [] 
    final_output_list_eu = []
    final_output_list_na = []
    final_output_list_latam = []
    final_output_list_africa = []
    final_output_list_unknown = []
    full_name = {'AS' : 'APAC', 'NA' : 'North America', \
'SA' : 'LATAM', 'AF' : 'Africa', 'EU' : 'EMEA', 'Unknown' : 'Unknown'}


    group_name = 'ambassadors'
    username = 'fedoradummy'
    password = '{{ fedoraDummyUserPassword }}'
#    username = raw_input('Username: ').strip()
#    password = getpass.getpass('Password: ')    
{% if env == "staging" %}
    base_url = 'https://admin.stg.fedoraproject.org/accounts/'
{% else %}
    base_url = 'https://admin.fedoraproject.org/accounts/'
{% endif %}

    fas = AccountSystem(base_url=base_url, username=username, password=password, timeout=600)

    # Call fedoraproject API with mwclient
{% if env == "staging" %}
    site = mwclient.Site(('https', 'stg.fedoraproject.org'), path='/w/') 
{% else %}
    site = mwclient.Site(('https', 'fedoraproject.org'), path='/w/') 
{% endif %}

    site.login(username, password) # Optional
    # Specify which page to edit
    page = site.Pages['Ambassadors/MembershipService/Verification2']

    #delete all the erswhile contents.
    page.text()
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
                if status == 'inactive':
                    inactive_list.append(user_name)
            #print 'match'
                elif status == 'active': #filter out all inactive accounts
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
        elif continent_code == 'AF':
            final_output_list_africa.append(item)
        elif continent_code == 'Unknown':
            final_output_list_unknown.append(item)
   # sort the list according to countries
    
    final_string = ''
    for final_output_list in [final_output_list_as, final_output_list_africa, \
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
                final = "<tr><td>%s</td><td> [[User:%s| %s]]</td><td>%s</td></tr>" % (to_bytes(index), to_bytes(user_name), to_bytes(human_name), to_bytes(email))

                final_string = final_string + final
            final_string = final_string + '</table>'

    time = datetime.datetime.utcnow()
    page.text()
    page.save(final_string, summary = time)

{% raw %}
    note = "{{admon/note | Last Updated : %s UTC. %s active contributors \
listed here against %s total.}}" % (time, len(output), len(people_list))
{% endraw %}
    page = site.Pages['Ambassadors/MembershipService/VerificationStats']
    page.text()
    page.save(note, summary = time)

    page = site.Pages['Ambassadors/MembershipService/Inactives']
    page.text()
    page.save(inactive_list, summary = time)

if __name__ == "__main__":
    calc_list()
