#:indentSize=4:tabSize=4:noTabs=true:wrap=soft:
#http://trac.pjsip.org/repos/browser/pjproject/trunk/pjsip-apps/src/python/samples/call.py
#
# SIP call redirector.

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
        current_call.answer(302, "Not here", hdr_list="")
       
# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):

    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

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
    lib.init(log_cfg = pj.LogConfig(level=LOG_LEVEL, callback=log_cb))
    transport = lib.create_transport(pj.TransportType.UDP, 
                                     pj.TransportConfig(port=5060,bound_addr="",public_addr=""))
    # print "\nListening on", transport.info().host, "port", transport.info().port, "\n"
    lib.start()
    # acc_cfg = pjsua.AccountConfig()
    # acc_cfg.id = "sip:someuser@pjsip.org"
    # acc_cfg.reg_uri = "sip:pjsip.org"
    # acc_cfg.proxy = [ "sip:pjsip.org;lr" ]
    # acc_cfg.auth_cred = [ AuthCred("*", "someuser", "secretpass") ]
    # acc_cb = MyAccountCallback()
    # acc = lib.create_account(acc_cfg, cb=acc_cb)
    acc = lib.create_account_for_transport(transport, cb=MyAccountCallback())
    my_sip_uri = "sip:" + transport.info().host + \
                 ":" + str(transport.info().port)
    print "My SIP URI is", my_sip_uri
    while True:
        continue #running this shebang 

### Shutdown the library
    transport = None
    acc.delete()
    acc = None
    lib.destroy()
    lib = None

except pj.Error, e:
    print "Exception: " + str(e)
    lib.destroy()
    lib = None
