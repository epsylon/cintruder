#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
"""
This file is part of the cintruder project, https://cintruder.03c8.net

Copyright (c) 2012/2020 psy <epsylon@riseup.net>

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
import pycurl
from io import BytesIO

class CIntruderCurl(object):
    """
    Class to control curl on behalf of the application.
    """
    agent = 'Googlebot/2.1 (+http://www.google.com/bot.html)'
    referer = '127.0.0.1'
    proxy = None
    ignoreproxy = None

    def __init__(self, captcha="", ignoreproxy="", proxy=""):
        """
        Class init
        """
        self.handle = pycurl.Curl()
        self.verbosity = 0
        self.url = self.set_url(captcha)
        self.captcha = BytesIO()
        self.proxy = self.set_proxy(ignoreproxy, proxy)
        self.set_option(pycurl.SSL_VERIFYHOST, 0)
        self.set_option(pycurl.SSL_VERIFYPEER, 0)
        #self.set_option(pycurl.SSLVERSION, pycurl.SSLVERSION_SSLv3)
        self.set_option(pycurl.COOKIEFILE, '/dev/null')
        self.set_option(pycurl.COOKIEJAR, '/dev/null')
        self.set_option(pycurl.NETRC, 1)

    def set_url(self, url):
        """
        Set the url.
        """
        self.url = url
        self.set_option(pycurl.URL, self.url)
        return url

    def set_agent(self, agent):
        """
        Set the user agent.
        """
        self.agent = agent
        self.set_option(pycurl.USERAGENT, self.agent)
        return agent

    def set_referer(self, referer):
        """
        Set the referer.
        """
        self.referer = referer
        self.set_option(pycurl.REFERER, self.referer)
        return referer

    def set_proxy(self, ignoreproxy, proxy):
        """
        Set the proxy to use.
        """
        self.proxy = proxy
        self.ignoreproxy = ignoreproxy
        if self.ignoreproxy == 1:
            self.set_option(pycurl.PROXY, "")
        else:
            self.set_option(pycurl.PROXY, self.proxy)
        return proxy

    def set_verbosity(self, level):
        """
        Set the verbosity level.
        """
        self.set_option(pycurl.VERBOSE, level)

    def set_option(self, *args):
        """
        Set the given option.
        """
        self.handle.setopt(*args)

    def request(self):
        """
        Perform a request and returns the payload.
        """
        if self.agent:
            self.set_option(pycurl.USERAGENT, self.agent)
        if self.referer:
            self.set_option(pycurl.REFERER, self.referer)
        if self.proxy:
            self.set_option(pycurl.PROXY, self.proxy)
        if self.ignoreproxy:
            self.set_option(pycurl.PROXY, "")
        if self.url:
            self.set_option(pycurl.URL, self.url)
        self.set_option(pycurl.SSL_VERIFYHOST, 0)
        self.set_option(pycurl.SSL_VERIFYPEER, 0)
        self.handle.setopt(self.handle.WRITEFUNCTION, self.captcha.write)
        try:
            self.handle.perform()
            print("\n[Info] Getting captcha...")           
            return self.captcha
        except pycurl.error as error:
            try:
                errno, errstr = error
            except:
                errno, errstr = "unknown!", "unknown!"
            print('\n[Error] Connection error... '+ str(errstr))
            return "exit"
 
    def close(self):
        """
        Close the curl handle.
        """
        self.handle.close()
        self.captcha.close()

    def print_options(self):
        """
        Print selected options.
        """
        print("\n[-] Verbose: active")
        print("[-] HTTP User Agent: "+str(self.agent))
        print("[-] HTTP Referer: "+ str(self.referer))
        if self.ignoreproxy:
            print("[-] Proxy: No proxy!")
        else:
            print("[-] Proxy: "+ str(self.proxy))
        print("[-] URL: "+ str(self.url)+ "\n")
