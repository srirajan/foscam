#!/usr/bin/env python
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import sys
import datetime
import getopt
from time import sleep
import urllib
import signal

import utils
import creds
import config
import socket

def main():

    socket.setdefaulttimeout(config.url_timeout)
    opts, args = getopt.getopt(sys.argv[1:], "hdi:c:", ["help", "debug", "image-dir=", "camera-name="])

    _debug = False
    show_help = False

    image_dir = None
    camera_name = None;
    for o, a in opts:
        if o in("-d", "--debug"):
            _debug = True
        if o in("-h", "--help"):
            show_help = True
        if o in("-i", "--image-dir"):
            image_dir = a
        if o in("-c", "--camera-name"):
            camera_name = a

    if not os.path.isdir(image_dir):
        print "Image store directory " + image_dir + " does not exist. Aborting"
        sys.exit(-1)

    if camera_name == None:
        print "Please provide camera name with -c option"
        sys.exit(-1)

    error_count = 0
    email_sent = 0
    log_filename = camera_name + ".log"
    log_filepath = os.path.join(image_dir, log_filename)
    log = open(log_filepath,'a+')

    log.write("".join(["[", datetime.datetime.now().strftime('%x %X'), "]",
                              "Starting foscam for ", camera_name, "\n"]))
    try:
        while True:
            log.write
            ctr = 0
            fname_ctr = 0
            timestr = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            timedir = os.path.join(image_dir, timestr)
            os.makedirs(timedir)
            while ctr <int(config.rotate_interval):
                ctr = ctr + int(config.lapse_interval)
                fname_ctr = fname_ctr + 1
                fname = "%s/snap_%05d.jpg" % (timedir, fname_ctr)
                try:
                    urllib.urlretrieve(creds.url_pass, fname)
                except IOError:
                    log.write("Exception in urllib")
                    error_count = error_count + 1
                    log.write("Error count:" + str(error_count) + "\n")
                    if error_count > config.max_errors:
                        if email_sent == 0:
                            utils.send_email (config.report_from, config.report_to, "Error count reached on foscam", "Camera name:" +camera_name )
                            email_sent = email_sent + 1;

                sleep(int(config.lapse_interval))
            cmd = "convert -delay %s %s/snap_*.jpg  %s/lapse_%s.mp4 2>/dev/null" % (config.lapse_interval, timedir, timedir, timestr)
            if _debug:
                print cmd
            os.system(cmd)
            cmd = "chmod 644 %s/lapse_%s.mp4" % (timedir,timestr)
            if _debug:
                print cmd
            os.system(cmd)
        log.close()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Gracefully exiting.")
        log.close()
        sys.exit(0)



if __name__ == "__main__":
    main()

