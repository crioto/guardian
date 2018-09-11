import requests
import sys
import os
import json

host = 'flink.guardian.optdyn.com'

class Flink():

    hostname = ''

    # Constructor
    def __init__(self, host):
        self.hostname = host


    # Retrieve configuration from /config REST Endpoint
    def Config(self):
        r = requests.get(self.ep('config'))
        return json.loads(r.content)


    # Request service overview (/overview)
    def Overview(self):
        r = requests.get(self.ep('overview'))
        return json.loads(r.content)


    # Upload new JAR. Full path to JAR file must be provided
    def Upload(self, jarfile):
        filename = os.path.basename(jarfile)

        with open(jarfile, 'rb') as f:
            headers = {
                'Content-Disposition': 'form-data',
                'name': 'jarfile',
                'filename': filename,
                'ContentType': 'application/x-java-archive'
            }
            r = requests.post(self.ep('jars/upload'), files={'filename': f}, headers=headers)
            return json.loads(r.content)

        return json.loads('{"status": "failure"}')


    def Run(self, jarfile):
        filename = os.path.basename(jarfile)

        r = requests.post(self.ep('jars/')+filename+'/run')
        return json.loads(r.content)


    def ep(self, suffix): 
        return 'http://'+self.hostname + '/' + suffix


flink = Flink(host)
config = flink.Config()
print("Flink Version: " + config['flink-version'] + ' ' + config['flink-revision'])
print("Timezone: " + config['timezone-name'] + ' ' + str(config['timezone-offset']))
print('Refresh Interval: ' + str(config['refresh-interval']))
overview = flink.Overview()
print('Taskmanagers: ' + str(overview['taskmanagers']))
print('Total slots: ' + str(overview['slots-total']))
print('Available slots: ' + str(overview['slots-available']))
print('Runnins jobs: ' + str(overview['jobs-running']))
print('Finished jobs: ' + str(overview['jobs-finished']))
print('Cancelled jobs: ' + str(overview['jobs-cancelled']))
print('Failed jobs: ' + str(overview['jobs-failed']))
print('')


if len(sys.argv) < 2: 
    print("Please specify path to JAR file")
    exit(1)


print("Uploading " + sys.argv[1])
upload = flink.Upload(sys.argv[1])
if upload['status'] == 'failure':
    print("Failed to upload JAR: Error unknown")
    exit(1)

print("Uploaded with status: " + upload['status'] + ' (' + upload['filename'] + ')')
if upload['status'] != 'success':
    print("Terminating")
    exit(2)

print("Starting job")
run = flink.Run(upload['filename'])
if 'jobid' in run:
    print("Started job with ID " + run['jobid'])

if 'errors' in run:
    print("Failed to run job:")
    for e in run['errors']:
        print(" - " + e)