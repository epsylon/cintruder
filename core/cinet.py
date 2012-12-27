#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
CIntruderNet distributed dictionary.

Publish results on social networking sites. 
             
This implementation is for identi.ca (http://identi.ca)
and twitter (http://twitter.com/)

This bot is completly Public. All publised data will be accessed from Internet 

Please report your results using -automatic- format to create a good distributed 
dicionary for brute forcing tasks. 
								             
cintrudernet: 
http://identi.ca/cintrudernet

cintrudernet (twitter clon): 
http://twitter.com/cintrudernet

To launch you own -bot-, first create an account on identica/twitter, 
and after change this values with your data:

   - username = <identica username>
   - password = <identica password>

Dont forget to put your bot to "follow" other -replicants-.
If you dont know any, try this: cintrudernet
-----
This file is part of the cintruder project, http://cintruder.sourceforge.net.

Copyright (c) 2012/2015 psy <root@lordepsylon.net> - <epsylon@riseup.net>

cintruder is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation version 3 of the License.

cintruder is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along
with cintruder; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import httplib, urllib
import base64

class CInet(object):

    def __init__(self, cintruder):
        # initialize main cintruder
        self.instance = cintruder

    def send_to_identica(self, msg, username, password, url=None):
        if url is None:
            url = "http://identi.ca/api/statuses/update.xml"
        data = urllib.urlencode({'status' : msg})
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        authorizationString = "Basic " + base64string
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain", "Authorization" : authorizationString}
        connection = httplib.HTTPConnection("identi.ca")
        connection.request("POST", "/api/statuses/update.xml", data, headers)
        response = connection.getresponse()
        print "\nINFO  :", response.status, response.reason 

if __name__ == "__main__":
    publish = CInet(object)
    publish.send_to_identica('#cintruder v0.2 - Distributed Online Dictionary - info: https://cintruder.sf.net/cinet', 'cintrudernet', '872ggF/f_:fUc4', 'http://identi.ca/api/statuses/update.xml')
