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
import optparse

class CIntruderOptions(optparse.OptionParser):
    def __init__(self, *args):
        optparse.OptionParser.__init__(self, 
                           description='Captcha Intruder is a pentesting tool to brute force captchas',
                           prog='cintruder.py',
			   version='\nCIntruder v0.2 - 2012 - (GPLv3.0) -> by psy\n',
                           usage= '\n\ncintruder [OPTIONS]')

        self.add_option("-v", "--verbose", action="store_true", dest="verbose", help="active verbose mode output results")
        self.add_option("--proxy", action="store", dest="proxy", help="use proxy server (tor: http://localhost:8118)")
        self.add_option("--track", action="store", dest="track", help="download a number of captchas from url (to: 'inputs/')")
        self.add_option("--train", action="store", dest="train", help="apply common OCR techniques to captcha")
        self.add_option("--crack", action="store", dest="crack", help="brute force using local dictionary (from: 'iconset/')")
        self.add_option("--xml", action="store", dest="xml", help="export result to xml format")

        group1 = optparse.OptionGroup(self, "Advanced OCR (training)")
        group1.add_option("--set-id", action="store", dest="setids", help="set colour's id manually (use -v for details)")
        group1.add_option("--editor", action="store_true", dest="editor", help="launch an editor to apply image filters")
        self.add_option_group(group1)

        group2 = optparse.OptionGroup(self, "Modules (training)")
        group2.add_option("--list", action="store_true", dest="listmods", help="list available modules (from: 'core/mods/')")
        group2.add_option("--mod", action="store", dest="name", help="train using a specific OCR exploiting module")
        self.add_option_group(group2)

        group3 = optparse.OptionGroup(self, "Handlering (cracking)")
        group3.add_option("--tool", action="store", dest="command", help="replace suggested word on commands of another tool. use 'CINT' marker like flag (ex: 'txtCaptcha=CINT')")
        self.add_option_group(group3)

        group4 = optparse.OptionGroup(self, "CIntruderNet ('http://cintruder.sf.net/cinet')")
        group4.add_option("--send-net", action="store_true", dest="sendnet", help="send resolved captcha to CIntruderNet")
        group4.add_option("--view-net", action="store_true", dest="viewnet", help="visit distributed online dictionary website")
        self.add_option_group(group4)

    def get_options(self, user_args=None):
        (options, args) = self.parse_args(user_args)
        options.args = args
        if (not options.train and not options.crack and not options.track and not options.listmods and not options.viewnet):
            print '='*75
            print  self.version
            print  self.description, "\n"
            print '='*75, "\n"
            print "Project site:"
            print "http://cintruder.sf.net", "\n"
            print "IRC:"
            print "irc.freenode.net -> #cintruder", "\n"
            print "Mailing list:"
            print "cintruder-users@lists.sf.net", "\n"
            print '='*75
            print "\nFor HELP use -h or --help\n"
            print '='*55, "\n"
            return False
        return options

