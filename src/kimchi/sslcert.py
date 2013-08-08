#
# Project Kimchi
#
# Copyright IBM, Corp. 2013
# Copyright (C) 2004-2005 OSAF. All Rights Reserved.
#
# Authors:
#  Adam Litke <agl@linux.vnet.ibm.com>
#  Toby Allsopp <toby@MI6.GEN.NZ>
#
# Portions of this file were derived from the python-m2crypto unit tests:
#     http://svn.osafoundation.org/m2crypto/trunk/tests/test_x509.py
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from M2Crypto import X509, EVP, RSA, ASN1
import time


class SSLCert(object):
    def __init__(self):
        req, pk = self._mkreq(1024)
        pkey = req.get_pubkey()
        sub = req.get_subject()
        self.cert = X509.X509()
        sn = int(time.time()) % (2 ** 32 - 1)
        self.cert.set_serial_number(sn)
        self.cert.set_version(2)
        self.cert.set_subject(sub)
        t = long(time.time()) + time.timezone
        now = ASN1.ASN1_UTCTIME()
        now.set_time(t)
        nowPlusYear = ASN1.ASN1_UTCTIME()
        nowPlusYear.set_time(t + 60 * 60 * 24 * 365)
        self.cert.set_not_before(now)
        self.cert.set_not_after(nowPlusYear)
        issuer = X509.X509_Name()
        issuer.CN = 'Kimchi Project'
        issuer.O = 'The Kimchi Project'
        self.cert.set_issuer(issuer)
        self.cert.set_pubkey(pkey)
        self.cert.sign(pk, 'sha1')
        assert self.cert.verify()
        assert self.cert.verify(pkey)

    def cert_text(self):
        return self.cert.as_text()

    def cert_pem(self):
        return self.cert.as_pem()

    def key_pem(self):
        return self._key

    def _mkreq(self, bits):
        def keygen_cb(*args):
            pass
        def passphrase_cb(*args):
            return ''
        pk = EVP.PKey()
        x = X509.Request()
        rsa = RSA.gen_key(bits, 65537, keygen_cb)
        pk.assign_rsa(rsa)
        self._key = rsa.as_pem(None, callback=passphrase_cb)
        rsa = None
        x.set_pubkey(pk)
        name = x.get_subject()
        name.C = "US"
        name.CN = "Kimchi Project"
        x.sign(pk,'sha1')
        assert x.verify(pk)
        return x, pk

def main():
    c = SSLCert()
    print c.cert_text()
    print c.cert_pem()
    print c.key_pem()

if __name__ == '__main__':
    main()
