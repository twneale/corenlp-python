import os

import zmq

from corenlp.models import CoreNLP


class Service:
    default_annotators = 'tokenize,ssplit,pos,lemma,parse'

    def __init__(self):
        self._broker_host = os.environ.get('CORENLP_BROKER_HOST', 'localhost')
        print('corenlp connecting to host: %r' % self._broker_host)
        self._broker_port = os.environ.get('CORENLP_BROKER_PORT', '5559')
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://%s:%s" % (self._broker_host, self._broker_port))

    def send(self, string, annotators=None):
        obj = dict(annotators=self.default_annotators, text=string)
        self.socket.send_json(obj)
        message = self.socket.recv_json()
        return CoreNLP(message)
