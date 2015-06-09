### Author: Alban Dumouilla
# Published June 9th, 2015

# Usage : python mailtester.py "streak_stage_name"
# This script outputs a CSV file that you can import in Streak for GMAIL to create boxes automatically from valid email adresses.
# Its input needs to be a CSV file called "inputlist.csv" in this format: 

# Company,Domain,First Name,Last Name
# The script will test several combinations of possible emails and validate it against the domain's MX server
# The output can be directly imported in Streak and will create Lead generation/CRM boxes automatically

from validate_email import validate_email
from urlparse import urlparse
from datetime import datetime
from random import randint
import time
import csv
import threading
import sys

startTime = datetime.now()
valid = []
failed = {}

print 'Processing, please wait...'

try:
    streak_stage = sys.argv[1]
    print "Streak stage: streak_stage"
except IndexError:
    print "Usage : python mailtester.py stagename (e.g. python mailtester.py start-up)"
    exit()
except Exception as e:
    print "Unhandled exception"
    print e
    exit()

def worker(first_name_orig, last_name_orig, domain, company_name):
    first_name = first_name_orig.lower()
    last_name = last_name_orig.lower()
    emails = [
                first_name,
                last_name,
                first_name+last_name,
                first_name+'.'+last_name,
                last_name+'.'+first_name,
                first_name[:1]+last_name,
                first_name+last_name[:1]
            ]      

    for x in emails:
        email = x+'@'+domain
        time.sleep(randint(0,9))
        try:
            print "Testing %s" % email
            is_valid = validate_email(email, verify=True)
            if is_valid == True:
                print "VALID : %s" % email
                valid.append({'email': email, 'first_name':first_name_orig, 'last_name':last_name_orig, 'company_name':company_name})
            elif is_valid == False:
                failed[email] = 'Not Valid'
        except Exception as e:
            failed[email] = str(e)


with open('inputlist.csv', 'rU') as csvfile:
    inputlist = csv.reader(csvfile, delimiter=',')
    i = 0
    for row in inputlist:
        if i > 0:
            om = row
            company_name = om[0]
            domain = om[1]
            first_name = om[2]
            last_name = om[3]
            stripped_domain = domain.replace('www.', '')

            t = threading.Thread(target=worker, args=(first_name, last_name, stripped_domain, company_name))
            t.start()

        i += 1

# Wait for all workers
main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()

print "Writing CSV output,,,"
with open('valid.csv','wb') as f:
    w = csv.writer(f)
    w.writerow(['Email', 'Name', 'Firstname', 'Lastname', 'Stage'])
    for item in valid:
        w.writerow([item['email'], item['company_name'], item['first_name'], item['last_name'], streak_stage])

with open('failed.csv','wb') as f:
    w = csv.writer(f)
    w.writerow(['Email', 'Status'])
    w.writerows(failed.items())


print 'Done!'
print (datetime.now()-startTime)
