"""Access and manipulate netgroup records in LDAP using RFC 2307 nisNetgroup objectclasses.
"""

def find(ldapobj, host='*', user='*', domain='*'):
    """Searches LDAP for netgroups having the specified host, user and domain.
    Any of the previous can be left out, which results in a wildcard that
    matches any value. Requires an object like ldap.LDAPObject (or a partial
    function with base and scope populated)."""

    filter = '(&(objectclass=nisNetgroup)(netNetgroupTriple=(%s,%s,%s)' % \
            (host, user, domain)
#    ldapobj.search(
