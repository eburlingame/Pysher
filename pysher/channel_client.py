import sys
import time
from pysher.pusher import Pusher
from json import dumps, loads

class ChannelClient:
    """Reads and writes from a single, secure pusher channel"""

    def __init__(self, config, channel, callback_fn):
        """Config is a dictionary with app-id, key, secret"""
        self.channel = channel
        self.callback_fn = callback_fn
        
        self.pusher_socket = Pusher(config['key'],
                                    secure = True,  
                                    secret = config['secret'], 
                                    custom_host="ws-us2.pusher.com")
                
        self.pusher_socket.connection.bind('pusher:connection_established', self._connect_handler)
        self.pusher_socket.connect()
    
    def send_message(self, message):
        """Sends a single event"""
        self.pusher_socket.connection.send_event('client-event', {'message': message}, self.channel)
    
    def _callback(self, data):
        d = loads(data)
        self.callback_fn(d['message'])
    
    def _connect_handler(self, data):
        channel = self.pusher_socket.subscribe(self.channel)
        channel.bind('client-event', self._callback)
        print("Connected to %s channel" % self.channel)