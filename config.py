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

smtp_server = 'smtp.mailgun.org'
smtp_port = 587
smtp_user = 'mailer@tty0.me'


report_from = 'mailer@tty0.me'
report_to = ['sriram.rajan@gmail.com']
report_subject = 'Foscam Error Report'

url_timeout = 5
lapse_interval = "2"  #seconds 
rotate_interval = "3600" #combined with the LAPSEINTERVAL to determine when to rotate
max_errors = 25;
