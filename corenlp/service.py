import zmq

from corenlp.models import CoreNLP


class Service:
    default_annotators = 'tokenize,ssplit,pos,lemma,parse'

    self._broker_host = os.environ['CORENLP_BROKER_HOST']
    self._broker_port = os.environ['CORENLP_BROKER_PORT']

    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5559")

    def send(self, string, annotators=None):
        obj = dict(annotators=self.default_annotators, text=string)
        self.socket.send_json(obj)
        message = self.socket.recv_json()
        return CoreNLP(message)
