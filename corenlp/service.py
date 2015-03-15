import sys
import zmq


class Service:
    default_annotators = 'tokenize,ssplit,pos,lemma,parse'

    def __init__(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5559")

    def send(self, string, annotators=None):
        obj = dict(annotators=self.default_annotators, text=string)
        socket.send_json(obj)
        message = socket.recv_json()
        return message
