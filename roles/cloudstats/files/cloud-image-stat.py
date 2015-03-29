from glob import glob
from datetime import date
from os import walk,listdir
from os.path import exists
from bz2 import BZ2File
import smtplib
from email.mime.text import MIMEText

stat_qcow2_x86_64 = 0
stat_rawxz_x86_64 = 0
stat_qcow2_i386 = 0
stat_rawxz_i386 = 0
stat_x86_64 = 0
stat_i386 = 0
stat_qcow2 = 0
stat_rawxz = 0
email_sender = 'cloud-image-stat-cron@fedoraproject.org'
email_receiver = 'cloud@lists.fedoraproject.org'
log_file = 'download.fedoraproject.org-access.log.bz2'

proxy_logs = glob('/var/log/hosts/proxy*')
date = date.today()
year,month,day = date.isoformat().split('-')

if month == '01':             # in case it is january
    qyear = str(date.year-1)
    qmonth = '12'
else:                         # for all other months
    qyear = year
    qmonth = str(date.month-1)

if int(qmonth) < 10:
    qmonth = '0'+qmonth

for proxy_log in (proxy_log for proxy_log in proxy_logs if '.stg.' not in proxy_log):
    proxy_month_log = '{0}/{1}/{2}'.format(proxy_log,qyear,qmonth)
    if exists(proxy_month_log):
        for day in listdir(proxy_month_log):
            proxy_download_log = '{0}/{1}/{2}/{3}'.format(proxy_month_log,day,'http',log_file)
            if exists(proxy_download_log):
                fd = BZ2File(proxy_download_log,'r')
                try:
                    for line in fd:
                        if 'sda.qcow2' in line:
                            if 'x86_64' in line:
                                stat_qcow2_x86_64 += 1
                            elif 'i386' in line:
                                stat_qcow2_i386 += 1
                        elif 'sda.raw.xz' in line:
                            if 'x86_64' in line:
                                stat_rawxz_x86_64 += 1
                            elif 'i386' in line:
                                stat_rawxz_i386 += 1
                finally:
                    fd.close()

stat_x86_64 = stat_qcow2_x86_64 + stat_rawxz_x86_64
stat_i386 = stat_qcow2_i386 + stat_rawxz_i386
stat_qcow2 = stat_qcow2_x86_64 + stat_qcow2_i386
stat_rawxz = stat_rawxz_x86_64 + stat_rawxz_i386

report = '''Download statistics for cloud images in month {0}-{1} :\n
- 32-bit arch :\n
    total = {2},  qcow2 = {3},  raw.xz = {4}\n
- 64-bit arch :\n 
    total = {5}, qcow2 = {6}, raw.xz = {7}\n
- qcow2 images :\n
    total = {8}, 32-bit = {9}, 64-bit = {10}\n
- raw.xz images :\n
    total = {11}, 32-bit = {12}, 64-bit = {13}\n'''

report = report.format(qmonth, qyear,
                       stat_i386, stat_qcow2_i386, stat_rawxz_i386,
                       stat_x86_64, stat_qcow2_x86_64, stat_rawxz_x86_64,
                       stat_qcow2, stat_qcow2_i386, stat_qcow2_x86_64,
                       stat_rawxz, stat_rawxz_i386, stat_rawxz_x86_64)

email = MIMEText(report)
email['Subject'] = 'Monthly download statistics for cloud images'
email['From'] = email_sender
email['To'] = email_receiver
server = smtplib.SMTP('localhost')
server.sendmail(email_sender,email_receiver,email.as_string())
server.quit()
