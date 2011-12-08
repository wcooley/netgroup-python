"""Common netgroup functions that are available on most Unix systems.

From the Linux man page v3.23 for *netgrent(3):

    The netgroup is a SunOS invention. A netgroup database is a list of string
    triples (hostname, username, domainname) or other netgroup names.  Any of
    the elements in a triple can be empty, which means that anything matches.
    The functions described here allow access to the netgroup databases. The
    file /etc/nsswitch.conf defines what database is searched.

There are several implementations of this available on the net, but this one
uses ctypes and hence requires no C compilation. It does, however, only work on
Python 2.5 and later.

The original implementation was by "bioinformed" and posted as a comment here:

http://planetjoel.com/viewarticle/629/Python+NSS+netgroups+interface

"""

from ctypes import CDLL,c_char_p
from ctypes import byref as _byref

import sys

if sys.platform.startswith('linux'):
    _libc_name = 'libc.so.6'
elif sys.platform == 'sunos5':
    _libc_name = 'libc.so'
elif sys.platform == 'darwin':
    _libc_name = 'libc.dylib'
else:
    raise NotImplementedError, 'Unsupported platform: ' + sys.platform

def getgroup(name):
    '''
    getgroup(netgroupName)

    Retrieve a netgroup using NSS routines
    Returns a list of matching (host,user,domain) tuples
    '''
    host,user,domain = c_char_p(None),c_char_p(None),c_char_p(None)

    libc = CDLL(_libc_name)

    libc.setnetgrent(name)

    try:
        groups = []
        while libc.getnetgrent(_byref(host), _byref(user), _byref(domain)):
            groups.append( (host.value,user.value,domain.value) )
        return groups

    finally:
        libc.endnetgrent()

def innetgr(netgroup,host=None,user=None,domain=None):
    '''
    innetgr(netgroup,host=host,user=user,domain=domain) -> bool

    Ask whether a host/user/domain tuple is part of a netgroup
    If no host,user or domain is passed then it returns true if the netgroup exists
    '''
    libc = CDLL(_libc_name)
    return bool(libc.innetgr(netgroup,host,user,domain))
