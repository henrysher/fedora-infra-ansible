#!/usr/bin/python


#    This script is for generating output for ambassadors map like this
#    http://fedoraproject.org/membership-map

#    Copyright (C) 2009, Susmit Shannigrahi, Susmit AT fedoraproject DOT org
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import getpass
from fedora.client.fas2 import AccountSystem
import GeoIP
import cPickle as pickle
import codecs
import datetime



def calc_list():
    '''Generate the ambassadors map data'''
    output = []
    people_list = []
    flag = 0    
        
    group_name = 'ambassadors'
    
    username = 'fedoradummy'
    password = '{{ fedoraDummyUserPassword }}'

{% if env == "staging" %}
    base_url = 'https://admin.stg.fedoraproject.org/accounts/'
{% else %}
    base_url = 'https://admin.fedoraproject.org/accounts/'
{% endif %}

    fas = AccountSystem(base_url=base_url, username=username, password=password)

    print 'Generating data file. Wait...'

    
    # Get a dictinary of all people in FAS
    data = fas.people_by_key(key='id', search=u'*', fields=['human_name', \
    'username', 'email', 'status', 'country_code', 'latitude', 'longitude'])
#    print data
    #get all data from a group
    group_people = fas.group_members(group_name)
    
    #make a list of usernames of a group    
    for item in group_people:
        people_list.append(item['username'])
        
    # get the country list from GeoIP 
    countries = dict(GeoIP.country_names.items())
    #print countries   
       
    for person in people_list:
       # print person
        for item in data.values():
            user_name = item['username']
            human_name = item['human_name']
            country_code = item['country_code']
            status = item['status']
            email = item['email']
            latitude = item['latitude']
            latitude = str(latitude)              
            longitude = item['longitude']   
            longitude = str(longitude)   
            

                  
                        
            if person == user_name:
            #print 'match'
                if status == 'active': #filter out all inactive accounts

                #different values for blank or non-blank fields are
                #_____________________________#                
                # Country Code  || Human Name #
                #_____________________________#
                # None          || None/Name  #
                # '   '         || None/Name  #
                # 'IN','FR' etc.|| None/Name  #
                #_____________________________#   
                
                    if latitude != 'None': 
                        if longitude != 'None': #if lat/long is not provided
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
                                    entry = [user_name, user_name, 'Unknown', email, latitude, longitude]
                                    output.append(entry)    
                                elif flag == 2: 
                                    entry = [user_name, human_name, 'Unknown', email, latitude, longitude]
                                    output.append(entry)
                                elif flag == 3:         
                                    entry = [user_name, user_name, country, email, latitude, longitude]
                                    output.append(entry)
                                else:
                                    entry = [user_name, human_name, country, email, latitude, longitude]
                                    output.append(entry)                    
    
                    #print entry

    #open the data file. Be cautions to open as unicode supported.
    output_file = codecs.open('/srv/web/membership-map/ambassadors_location.txt', encoding='utf-8', mode='w+')

    

    # write the format, one can also add an "icon" field after description.
    #output_file.write('point\ttitle\tdescription\n')
    output_file.write('point\ttitle\tdescription\ticon\ticonSize\n')

    # write fas data.
    for item in output:
        output_data = '%s,%s\t<a href=\"http://fedoraproject.org/wiki/user:%s\"target="_blank">%s</a>\t<br> Email: %s AT fedoraproject DOT org <br> Country:%s\t./f-dot.png\t15,15\n'% (item[4], item[5], item[0], item[1], item[0], item[2])
        output_file.write(output_data)
    output_file.close()       


if __name__ == "__main__":
    calc_list()


