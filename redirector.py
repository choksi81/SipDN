
# This module will answer a SIP INVITE with a 302 Moved Temporarily or 403 Forbidden
# http://www.cisco.com/c/en/us/td/docs/voice_ip_comm/sip/proxies/1-0/administration/guide/ver1_0/appbcf.html

import pjsua as pj
LOG_LEVEL = 3
current_call = None

def log_cb(level, str, len):
    print str,

class MyAccountCallback(pj.AccountCallback):
    def __init__(self, account=None):
        pj.AccountCallback.__init__(self, account)
    def on_incoming_call(self, call):
        #need to perform our stuff here
        #call.info().remote_uri
        call.answer(302, "Moved temporarily")
        #call.answer(403)
        #pass

try:
    lib = pj.Lib()
    lib.init(log_cfg = pj.LogConfig(level=LOG_LEVEL, callback=log_cb))
except pj.Error, e:
    print "Lib init exception: " + str(e)
    lib.destroy()
    lib = None

try:    
    transport = lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(0))
    print "\nListening on", transport.info().host, 
    print "port", transport.info().port
except pj.Error, e:
    print "Transport exception: " + str(e)
    lib.destroy()
    lib = None

try:
    lib.start()
except pj.Error, e:
    print "Lib start exception: " + str(e)
    lib.destroy()
    lib = None

try:
    acc_cfg = pj.AccountConfig()
    acc_cfg.id = "sip:redirector@sipdn.local"
    acc_cb = MyAccountCallback()
    acc = lib.create_account(acc_cfg, cb=acc_cb)

except pj.Error, e:
    print "Account exception: " + str(e)
    lib.destroy()
    lib = None

#:indentSize=4:tabSize=4:noTabs=true:wrap=soft: