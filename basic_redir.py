#:indentSize=4:tabSize=4:noTabs=true:wrap=soft:
#http://trac.pjsip.org/repos/browser/pjproject/trunk/pjsip-apps/src/python/samples/call.py
# $Id$
#
# SIP call sample.
#
# Copyright (C) 2003-2008 Benny Prijono <benny@prijono.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
import sys
import pjsua as pj

LOG_LEVEL=3
current_call = None

# Logging callback
def log_cb(level, str, len):
    print str,


# Callback to receive events from account
class MyAccountCallback(pj.AccountCallback):
    def __init__(self, account=None):
        pj.AccountCallback.__init__(self, account)

    def on_incoming_call(self, call):
        global current_call
        if current_call:
            call.answer(486, "Busy")
            return
        print "Incoming call from ", call.info().remote_uri
        current_call = call
        call_cb = MyCallCallback(current_call)
        current_call.set_callback(call_cb)
        current_call.answer(302)

       
# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):

    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    # Notification when call state has changed
    def on_state(self):
        global current_call
        print "Call with", self.call.info().remote_uri,
        print "is", self.call.info().state_text,
        print "last code =", self.call.info().last_code, 
        print "(" + self.call.info().last_reason + ")"
       
        if self.call.info().state == pj.CallState.DISCONNECTED:
            current_call = None
            print 'Current call is', current_call

# Create library instance
lib = pj.Lib()

try:
    # Init library with default config and some customized
    # logging config.
    lib.init(log_cfg = pj.LogConfig(level=LOG_LEVEL, callback=log_cb))

    # Create UDP transport which listens to any available port
    transport = lib.create_transport(pj.TransportType.UDP, 
                                     pj.TransportConfig(port=5060,bound_addr="",public_addr=""))
    print "\nListening on", transport.info().host, 
    print "port", transport.info().port, "\n"
   
    # Start the library
    lib.start()

    # Create local account
    acc = lib.create_account_for_transport(transport, cb=MyAccountCallback())

    # If argument is specified then make call to the URI
    # if len(sys.argv) > 1:
        # lck = lib.auto_lock()
        # current_call = make_call(sys.argv[1])
        # print 'Current call is', current_call
        # del lck

    my_sip_uri = "sip:" + transport.info().host + \
                 ":" + str(transport.info().port)

    print "My SIP URI is", my_sip_uri
    while True:
        continue
        #if not current_call:
            #continue
        #current_call.answer(302)


    # Shutdown the library
    transport = None
    acc.delete()
    acc = None
    lib.destroy()
    lib = None

except pj.Error, e:
    print "Exception: " + str(e)
    lib.destroy()
    lib = None
