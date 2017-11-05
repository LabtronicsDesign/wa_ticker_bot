# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 18:13:41 2017

@author: SPWC
"""

from yowsup.stacks                             import YowStackBuilder
from yowsup.common                             import YowConstants
from yowsup.layers                             import YowLayerEvent
from layer                                     import EchoLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.env                                import YowsupEnv

credentials = ("44XXXXXXXXX", "password") # Replace your mobile number and password here...
run_thru = 0
while __name__==  "__main__":
    run_thru=+1
    print(run_thru)
    try:
        stackBuilder = YowStackBuilder()
        stack = stackBuilder\
            .pushDefaultLayers(True)\
            .push(EchoLayer)\
            .build()

        stack.setCredentials(credentials)
        stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))          #sending the connect signal
        stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])           #whatsapp server address
        stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
        stack.setProp(YowCoderLayer.PROP_RESOURCE, YowsupEnv.getCurrent().getResource())  #info about us as WhatsApp client
        stack.loop(timeout = 0.5, discrete = 0.5 )                                        #this is the program mainloop

    except:
        print('error...Trying Again')
