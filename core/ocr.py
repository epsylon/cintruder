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
from PIL import Image
from operator import itemgetter
import os, hashlib, time, sys, subprocess, platform

class CIntruderOCR(object):
    """
    Class to apply OCR techniques into captchas
    """
    def __init__(self, captcha, options):
        # initialize main CIntruder
        try:
            im = Image.open(captcha)
            im2 = Image.new("P", im.size, 255)
            im = im.convert("P")
            if options.editor:
                im.show()
        except:
            print "Error during OCR process!. is that captcha supported?\n"
            return

        colourid = []
        hist = im.histogram()
        values = {}
        for i in range(256):
            values[i] = hist[i]
        for j, k in sorted(values.items(), key=itemgetter(1), reverse=True)[:10]:
            colourid.append(j)  
            if options.verbose:
                print "Colour ID:", j
                print "Total of pixels of that colour: ", k
                print "----------"
                print "================="

        temp = {}
        for x in range(im.size[1]):
            for y in range(im.size[0]):
                pix = im.getpixel((y, x))
                temp[pix] = pix
                if options.setids:
                    colourid = int(options.setids)
                    if pix == colourid:
                        im2.putpixel((y, x), 0)
                else:
                    if pix == colourid[1]: #id numbers of colours to get (*)
                        im2.putpixel((y, x), 0)

        if not os.path.exists("outputs/"):
            os.mkdir("outputs/")
        im2.save("outputs/last-ocr_image-processed.gif")

        inletter = False
        foundletter = False
        start = 0
        end = 0

        letters = []

        for y in range(im2.size[0]): 
            for x in range(im2.size[1]): 
                pix = im2.getpixel((y, x))
                if pix != 255:
                    inletter = True

            if foundletter == False and inletter == True:
                foundletter = True
                start = y

            if foundletter == True and inletter == False:
                foundletter = False
                end = y
                letters.append((start, end))
            inletter = False

        count = 0
        for letter in letters:
            m = hashlib.md5()
            im3 = im2.crop(( letter[0], 0, letter[1], im2.size[1] ))
            m.update("%s%s"%(time.time(), count))
            if not os.path.exists("outputs/words/"):
                os.mkdir("outputs/words/")
            im3.save("outputs/words/%s.gif"%(m.hexdigest()))
            count += 1

        print "OCR processing... "
        print "================="
        print "Training Results:"
        print "================="
        print "Number of 'words' extracted: ", count
        if count == 0:
            print "\nOuch!. Looks like this type of captcha is resisting to our OCR methods... by the moment ;)\n"
            print "To train better, try this...\n" 
            print "            1) Check colour's id values and quantity of pixels with --verbose option" 
            print "            2) Set different id values using --set-id and try to extract words again"
            print "            3) If you cannot extract nothing, try to apply image filters manually with the editor\n"
            print "Mailing list: cintruder-users@lists.sourceforge.net"
            print "------------\n"
        else:
            print "Output folder              : ", "outputs/words/\n"

            # checking for platform to list new words added to dictionary
            os_sys = platform.system()
            if os_sys == "Windows":
                subprocess.call("dir outputs/words/", shell=True)
            else:
                subprocess.call("ls outputs/words/", shell=True)

            if options.editor:
                im2.show()
            print "\nNow, move each image to the correct folder on your dictionary: '/iconset/'\n"

if __name__ == "__main__":
    if sys.argv[1:]:
        ocr = CIntruderOCR(sys.argv[1:])
        print ("Data correctly extracted!")
    else:
        print ("You must set a captcha to learn. ex: test.gif")
