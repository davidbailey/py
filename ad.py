import ldap
import pandas
import datetime.datetime
from ldap_paged_search import LdapPagedSearch

host = 'ldaps://example.com:636'
username = 'domain\\username'
password = 'password'

baseDN = 'DC=example,DC=com'
filter = "(&(objectCategory=computer))"
#attributes = ['dn']
attributes = ['*']

l = LdapPagedSearch(host, username, password, maxPages=0, pageSize=1000)
#ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
results = l.search(baseDN, filter, attributes = attributes)

computers = []
for computer in results:
    dn = computer[0]
    try:operatingSystem = computer[1]['operatingSystem'][0]
    except: operatingSystem = False
    try: operatingSystemServicePack = computer[1]['operatingSystemServicePack'][0]
    except: operatingSystemServicePack = False
    hostname = computer[1]['cn'][0]
    try: fqdn = computer[1]['dNSHostName'][0]
    except: fqdn = False
    whenCreated = computer[1]['whenCreated'][0]
    try: lastLogonTimestamp = datetime.datetime.utcfromtimestamp((int(computer[1]['lastLogonTimestamp'][0]) - 116444736000000000) / 10000000)
    except: lastLogonTimestamp = False
    try: description = computer[1]['description'][0]
    except: description = False
    GUID = computer[1]['objectGUID'][0]
    computers.append((dn,hostname,fqdn,operatingSystem,operatingSystemServicePack,whenCreated,lastLogonTimestamp,description,GUID))

comp = pandas.DataFrame(computers)
comp.columns = ['dn','hostname','fqdn','operatingSystem','operatingSystemServicePack','whenCreated','lastLogonTimestamp','description','GUID']
windows = comp[comp['operatingSystem'] != "Mac OS X"]
