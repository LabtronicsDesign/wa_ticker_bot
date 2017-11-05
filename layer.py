# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 18:13:41 2017

@author: SPWC
"""

from yowsup.layers.interface                           import YowInterfaceLayer                 #Reply to the message
from yowsup.layers.interface                           import ProtocolEntityCallback            #Reply to the message
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity         #Body message
from yowsup.layers.protocol_presence.protocolentities  import PresenceProtocolEntity            #Name presence
from yowsup.layers.network                             import YowNetworkLayer
from yowsup.layers                                     import YowLayerEvent
from core                                              import ticker_sym
from yowsup.layers.protocol_iq                         import YowIqProtocolLayer

from yowsup.layers.protocol_presence.protocolentities  import AvailablePresenceProtocolEntity   #Online
from yowsup.layers.protocol_presence.protocolentities  import UnavailablePresenceProtocolEntity #Offline
import os, time

name = "SPWC_Bot"

class EchoLayer(YowInterfaceLayer):
    
    @ProtocolEntityCallback("iq")
    def onIq(self, entity):
        pass
        
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            time.sleep(0.05)
            self.toLower(messageProtocolEntity.ack()) #Set received (double v)
            time.sleep(0.05)
            self.toLower(PresenceProtocolEntity(name = name)) #Set name Presence
            time.sleep(0.05)
            self.toLower(AvailablePresenceProtocolEntity()) #Set online
            time.sleep(0.05)
            self.toLower(messageProtocolEntity.ack(True)) #Set read (double v blue)
            time.sleep(0.05)
            self.onTextMessage(messageProtocolEntity) #Send the answer
            time.sleep(0.05)
            self.toLower(UnavailablePresenceProtocolEntity()) #Set offline
        elif messageProtocolEntity.getType() == 'media':
            self.toLower(messageProtocolEntity.ack()) #Set received (double v)

###########Added to check if Automatially reconnects###########
    @ProtocolEntityCallback("event")
    def onEvent(self, layerEvent):
        #log("WhatsApp-Plugin : EVENT " + layerEvent.getName())
        if layerEvent.getName() == YowNetworkLayer.EVENT_STATE_DISCONNECTED:
            print("WhatsApp-Plugin : Disconnected reason: %s" % layerEvent.getArg("reason"))
            if layerEvent.getArg("reason") == 'Connection Closed':
                time.sleep(5)
                print("WhatsApp-Plugin : Issueing EVENT_STATE_CONNECT")
                self.getStack().broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
            elif layerEvent.getArg("reason") == 'Ping Timeout' or 'Requested':
                time.sleep(5)
                print("WhatsApp-Plugin : Issueing EVENT_STATE_DISCONNECT")
                self.getStack().broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT))
                time.sleep(5)
                print("WhatsApp-Plugin : Issueing EVENT_STATE_CONNECT")
                self.getStack().broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
            else:
                time.sleep(5)
                print("WhatsApp-Plugin : Issueing EVENT_STATE_DISCONNECT")
                self.getStack().broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT))
                time.sleep(20)
                print("WhatsApp-Plugin : Issueing EVENT_STATE_CONNECT")
                self.getStack().broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        elif layerEvent.getName() == YowNetworkLayer.EVENT_STATE_CONNECTED:
            print("WhatsApp-Plugin : Connected")
###########End to check if Automatially reconnects###########

##########ACK Receipt###########
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())
##########ACK Receipt###########

##########Test Message###########
    def onTextMessage(self,messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            message    = messageProtocolEntity.getBody().upper()
            recipient  = messageProtocolEntity.getFrom()
            textmsg    = TextMessageProtocolEntity
            if message.startswith(('$','£','\u20ac','฿','\u0243')) and len(message.split()) == 1 and len(message) > 1:
                new_symbol = ticker_sym()
                if new_symbol.messaged_ticker(message)!=False: 
                    answer = new_symbol.messaged_ticker(message)
                else:
                    return
                self.toLower(textmsg(answer, to = recipient ))
            else:
                return

        elif message == '&re start':
                answer = "Ok "+", rebooting. Bye bye."
                self.toLower(textmsg(answer, to = recipient ))
                time.sleep(3)
                self.toLower(UnavailablePresenceProtocolEntity())
                time.sleep(2)
                os.system('reboot')

        elif message == '&shut down':
                answer = "Ok "+", shutting down. Bye bye."
                self.toLower(textmsg(answer, to = recipient ))
                time.sleep(3)
                self.toLower(UnavailablePresenceProtocolEntity())
                time.sleep(2)
                os.system("sudo shutdown -h now")

        else:
            return
##########Text Message###########



