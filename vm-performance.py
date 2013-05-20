#!/usr/bin/python
import os, sys, time
from novaclient.v1_1 import client
 
TEST_IMAGE = '5d9b28d7-b08e-457a-8674-99edf8c6a139'
NUM_SERVERS = 10
SERVER_NAME = 'br123'
WAIT_INTERVAL = 120
starttime= time.time()

def get_client():
    username = os.getenv('OS_USERNAME')
    tenant_name = os.getenv('OS_TENANT_NAME')
    password = os.getenv('OS_PASSWORD')
    auth_url = os.getenv('OS_AUTH_URL')
 
    return client.Client(username=username,
                         api_key=password,
                         project_id=tenant_name,
                         auth_url=auth_url)
 
def get_vms():
    search_opts="name=SERVER_NAME*"
    return client.servers.list(search_opts)


client =get_client()

# check for delete switch
# if found delete servers, if not found
#  Create X servers with name br123
if len(sys.argv) > 1:
   if sys.argv[1] == '-d': 
      servers=get_vms()
      for Server in servers:
         client.servers.delete(Server)
      sys.exit()
else:
   client.servers.create(SERVER_NAME, flavor=1, image=TEST_IMAGE, max_count=NUM_SERVERS)

# List all servers that start with br123
servers=get_vms()

for Server in servers:
  print Server.name, Server.id

print ""
print "Waiting: %s seconds..." % (WAIT_INTERVAL)
print ""

time.sleep(WAIT_INTERVAL)

# Re-aquire servers for updated status
servers=get_vms()

latest=0
# Print out the goodies
for Server in servers:
  print Server.id, Server.status, Server.updated
  if latest < Server.updated:
     latest = Server.updated

print "Start Time: %s" % starttime
print "Latest: %s" % latest
#print "Performance Metric (Last active - start-time): %s" (latest - starttime)
