#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
$Id$

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
import os, traceback, hashlib, sys, time
import platform, subprocess, re, webbrowser
from core.options import CIntruderOptions
from core.crack import CIntruderCrack
from core.curl import CIntruderCurl
from core.xml_export import CIntruderXML
from core.cinet import CInet
from urlparse import urlparse

# set to emit debug messages about errors (0 = off).
DEBUG = 1

class cintruder():
    """
    CIntruder application class
    """
    def __init__(self):
        self.captcha = ""
        self.optionOCR = []
        self.optionCrack = []
        self.optionParser = None
        self.optionCurl = None
        self.options = None
        self.word_sug = None
        self.train == 0
        self.crack == 0
        self.ignoreproxy = 1  
        self.isurl = 0

        self.os_sys = platform.system()
        self._webbrowser = webbrowser

        # connect to CIntruderNet"
        self.sn_service = 'https://identi.ca'
        self.sn_username = 'cintrudernet'
        self.sn_password = '872ggF/f_:fUc4'
        self.sn_url = 'http://identi.ca/api/statuses/update.xml'

    def set_options(self, options):
        """
        Set cintruder options
        """
        self.options = options

    def create_options(self, args=None):
        """
        Create the program options for OptionParser.
        """
        self.optionParser = CIntruderOptions()
        self.options = self.optionParser.get_options(args)
        if not self.options:
            return False
        return self.options

    def set_webbrowser(self, browser):
        self._webbrowser = browser

    @classmethod
    def try_running(cls, func, error, args=None):
        """
        Try running a function and print some error if it fails and exists with
        a fatal error.
        """
        args = args or []
        try:
            return func(*args)
        except Exception:
            print(error, "error")
            if DEBUG:
                traceback.print_exc()

    def get_attack_captchas(self):
        """
        Get captchas to brute force
        """
        captchas = []
        options = self.options
        p = self.optionParser

        if options.train:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print("Starting to 'train'")
            print('='*75)
            captchas = [options.train]

        if options.crack:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print("Starting to 'crack'")
            print('='*75)
            captchas = [options.crack]

        if options.track:
            print('='*75)
            print(str(p.version))
            print('='*75)
            print("Starting to 'track' from url...")
            print('='*75)
            captchas = [options.track]
            
        return captchas

    def train(self, captchas):
        """
        Learn mode:
            + Add words to the brute forcing dictionary
        """
        self.train_captcha(captchas)

    def train_captcha(self, captcha):
        """
        Learn mode:
            1- Apply OCR to the captcha to split into unities
            2- Recognize that unities like alphanumeric words
            3- Put words into dictionary
        """
        options = self.options
        
        # step 1: aplying OCR techniques (research required!)
        if options.name:
            print "Loading module:", options.name
            print "==============="
            try:
                sys.path.append('core/mods/%s/'%(options.name))
                exec("from " + options.name + "_ocr" + " import CIntruderOCR")
            except Exception:
                print "This module: '", options.name, "' exists?. Try --list to view available modules\n"
                sys.exit(2)
            self.optionOCR = CIntruderOCR(captcha, options)
        else:
            from core.ocr import CIntruderOCR
            self.optionOCR = CIntruderOCR(captcha, options)

        if options.setids:
            try:
                setids = int(options.setids)
                try: 
                    if setids >= 0 and setids <= 255:
                        self.optionOCR = CIntruderOCR(captcha, options)
                    else:
                        sys.exit(2)
                except:
                    sys.exit(2)     
            except:
                print "You must enter a correct number colour id value between 0 and 255\n"
                sys.exit(2)
        
        # step 2: recognize unities as words (research required!)

        # step 3: move to correct folder on dictionary

    def crack(self, captchas):
        """
        Crack mode:
            + Brute force target's captcha against a dictionary
        """
        self.crack_captcha(captchas)

    def crack_captcha(self, captcha):
        """
        Crack mode: bruteforcing...
        """
        options = self.options

        if options.name:
            print "Loading module:", options.name
            print "==============="
            try:
                sys.path.append('core/mods/%s/'%(options.name))
                exec("from " + options.name + "_crack" + " import CIntruderCrack")
            except Exception:
                print "This module: '", options.name, "' exists?. Try --list to view available modules\n"
                sys.exit(2)
            self.optionCrack = CIntruderCrack(captcha)
            w = self.optionCrack.crack(options)
            self.word_sug = w
        else:
            from core.crack import CIntruderCrack
            self.optionCrack = CIntruderCrack(captcha)
            w = self.optionCrack.crack(options)
            self.word_sug = w

    def remote(self, captchas, proxy):
        """
        Get remote captchas 
        """
        l = []
        for captcha in captchas:
            c = self.remote_captcha(captcha, proxy)
            l.append(c)
        return l

    def remote_captcha(self, captcha, proxy):
        """
        Get remote captcha
        """
        if proxy:
            self.ignoreproxy=0
        self.optionCurl = CIntruderCurl(captcha, self.ignoreproxy, proxy)
        buf = self.optionCurl.request()
        if buf != "exit":
            m = hashlib.md5()
            m.update(captcha)
            if not os.path.exists("inputs/"):
                os.mkdir("inputs/")
            h = "inputs/%s.gif"%(m.hexdigest())
            f = open(h, 'wb')
            f.write(buf.getvalue())
            f.close
            buf.close
            return h
        else:
            sys.exit(2)

    def export(self, captchas):
        """
        Export results
        """
        if self.options.xml and not (self.options.train):
            self.optionXML = CIntruderXML(captchas)
            if self.word_sug == None:
                print "XML NOT created!: There is not words to suggest"
            else:
                self.optionXML.print_xml_results(captchas, self.options.xml, self.word_sug)
                print "XML created:", self.options.xml
            print "------------\n"

    def track(self, captchas, proxy, num_tracks):
        """
        Download captchas from url
        """
        for captcha in captchas:
            self.track_captcha(captcha, proxy, num_tracks)

    def track_captcha(self, captcha, proxy, num_tracks):
        """
        This technique is usefull to create a dictionary with 'session based' captchas
        """
        options = self.options
        urlp = urlparse(captcha)
        self.domain = urlp.hostname
        if not os.path.exists("inputs/%s"%(self.domain)):
            os.mkdir("inputs/%s"%(self.domain))
        if proxy:
            self.ignoreproxy = 0
        buf = ""
        i=0
        while i < int(num_tracks) and buf != "exit":
            self.optionCurl = CIntruderCurl(captcha, self.ignoreproxy, proxy)
            buf = self.optionCurl.request()
            if options.verbose:
                print "[-]Connection data:"
                out = self.optionCurl.print_options()
                print '-'*45
            if buf != "exit":
                m = hashlib.md5()
                m.update("%s%s"%(time.time(), captcha))
                h = "inputs/%s/%s.gif"%(self.domain, m.hexdigest())
                f = open(h, 'wb')
                f.write(buf.getvalue())
                f.close
                buf.close
                print "Saved into:", h
                print "------------"
            i=i+1
        if buf != "exit":
            print "================="
            print "Tracking Results:"
            print "================="
            print "Number of 'captchas' tracked:", num_tracks, "\n"

    def run(self, opts=None):
        """ 
        Run cintruder
        """ 
        if opts:
            options = self.create_options(opts)
            self.set_options(options)
        options = self.options

        #step 0: list output results and get captcha targets
        if options.listmods:
            print "======================================="
            print "List of specific OCR exploiting modules"
            print "======================================="
            top = 'core/mods/'
            for root, dirs, files in os.walk(top, topdown=False):
                for name in files:
                    if name == 'DESCRIPTION':
                        if self.os_sys == "Windows": #check for win32 sys
                            subprocess.call("type %s/%s"%(root, name), shell=True)
                        else:
                            subprocess.call("cat %s/%s"%(root, name), shell=True)
            sys.exit(2)    

        captchas = self.try_running(self.get_attack_captchas, "\nInternal error getting -captchas-. look at the end of this Traceback.")
        captchas = self.sanitize_captchas(captchas)
        captchas2track = captchas

        if self.isurl == 1 and (options.train or options.crack):
            if options.proxy:
                captchas = self.try_running(self.remote, "\nInternal problems tracking: ", (captchas, options.proxy))
            else:
                captchas = self.try_running(self.remote, "\nInternal problems tracking: ", (captchas, ""))
            
            if options.verbose:
                print "[-] Connection data:"
                out = self.optionCurl.print_options()
                print '-'*45

        #step 0: track
        if options.track:
            if options.args: 
                try:
                    num_tracks = int(options.args[0])
                    try: 
                        if num_tracks >= 1:
                            num_tracks = int(num_tracks)
                        else:
                            sys.exit(2)    
                    except:
                        sys.exit(2)	
                except:
                    print "Track number parameter is not a valid integer\n"
                    sys.exit(2)
            else:
                num_tracks = int(5) # default track connections
            if options.proxy:
                self.try_running(self.track, "\nInternal problems tracking: ", (captchas2track, options.proxy, num_tracks))
            else:
                self.try_running(self.track, "\nInternal problems tracking: ", (captchas2track, "", num_tracks))

        #step 1: train
        if options.train:
            if len(captchas) == 1:
                for captcha in captchas:
                    if captcha is None:
                        print "\nError during OCR process!. is that captcha supported?\n"
                    else:
                        print "Target: ", options.train
                        print "======="
                        self.try_running(self.train, "\nInternal problems training: ", (captchas))   
            else:
                for captcha in captchas:
                    if len(captchas) > 1 and captcha is None:
                        pass
                    else:
                        print "Target: ", options.train
                        self.try_running(self.train, "\nInternal problems training: ", (captchas))
        if options.xml:
            print "XML NOT created!: Not necessary on train mode\n"
        
        #step 2: crack
        if options.crack:
            if len(captchas) == 1:
                for captcha in captchas:
                    if captcha is None:
                        print "\nError during Cracking process!. is that captcha supported?\n"
                    else:
                        print "Target: ", options.crack
                        print "======="
                        self.try_running(self.crack, "\nInternal problems cracking: ", (captchas))
            else:
                for captcha in captchas:
                    if len(captchas) > 1 and captcha is None:
                        pass
                    else:
                        print "Target: ", options.crack
                        print "======="
                        self.try_running(self.crack, "\nInternal problems cracking: ", (captchas))

            if options.command:
                print "INFO  : Executing tool connector... \n"
                if self.word_sug is not None:
                    print "This is the word suggested by CIntruder: [", self.word_sug, "] \n"
                else:
                    print "ERROR : CIntruder hasn't any word to suggest. Handlering tool process aborted! ;(\n"
                    sys.exit(2)
                if "CINT" in options.command: # check parameter CINT on command (*)
                    # change cintruder suggested word for the users captchas input form parameter
                    # and execute handlered tool with it.
                    if self.word_sug is not None:      
                        cmd = options.command.replace("CINT", self.word_sug)
                        #print cmd 
                        subprocess.call(cmd, shell=True)
                    else:
                        cmd = options.command
                        #print cmd
                        subprocess.call(cmd, shell=True)
                else:
                    print "ERROR : Captcha's parameter flag: 'CINT' is not on", options.command, "\n"

        #step 3: export
        if options.xml:
            self.try_running(self.export, "\nInternal problems exporting: ", (captchas))

        #step 4: publish - only when there is a broken captcha result and url source comes from Internet
        if options.sendnet and self.word_sug is not None and self.isurl == 1 and options.crack:
            m = hashlib.md5()
            m.update(options.crack + self.word_sug)
            print "Connecting to...           " + self.sn_service + "/" + self.sn_username
            print "Hashing broken captcha... ", m.hexdigest(), "\n"
            print "This is the word suggested by CIntruder: [", self.word_sug, "]" 
            c = raw_input("\nIs that word OK (Y/n)?")
            if c == "N" or c == "n":
                print "\nSo... Aborting!! :)\n"
                sys.exit(2)
            else:
                try:
                    sns_publish_results = CInet(self)
                    tags = '#cintruder '
                    msg = tags + m.hexdigest() + ' - target: ' + options.crack + ' | word: ' + self.word_sug
                    print "Sending...                ", msg
                    username = self.sn_username
                    password = self.sn_password
                    url = self.sn_url
                    sns_publish_results.send_to_identica(msg, username, password, url)
                    print "\nINFO  : Data published correctly! ;-)\n"
                except:
                    print "\nERROR : There are some errors publishing. Try again or report the bug. Thnks!\n"
                    sys.exit(2)

        if options.viewnet:
            self._webbrowser.open('http://cintruder.sf.net/cinet')

    def sanitize_captchas(self, captchas):
        """
        Sanitize correct input of source target(s)
        """
        options = self.options
        all_captchas = set()

        for captcha in captchas:
            # captcha from url
            if "http://" in captcha or "https://" in captcha:
                all_captchas.add(captcha)
                self.isurl = 1
            elif self.isurl == 0: # captcha from file
                (root, ext) = os.path.splitext(captcha)       
                if ext != '.gif' and ext != '.jpg' and ext != '.jpeg' and ext != '.png': #by the moment                    
                    captcha = None
                    all_captchas.add(captcha)
                else:
                    all_captchas.add(captcha)
                self.isurl = 0

        return all_captchas

if __name__ == "__main__":
    app = cintruder()
    options = app.create_options()
    if options:
        app.set_options(options)
        app.run()
