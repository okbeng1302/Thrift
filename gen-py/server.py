# coding:utf-8


import sys
sys.path.append("Hello")

from Hello import *
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import logging
from Hello.constants import *

logging.basicConfig(filename='logger.log', level=logging.INFO, format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class HelloService:

    def helloString(self, html):
        logging.info("start parse html")
        logging.info(html)
        return "1234"

def run():
    handler = HelloService()
    processor = Hello.Processor(handler)
    transport = TSocket.TServerSocket("127.0.0.1", 9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    logging.info('start thrift serve in python')
    server.serve()
    logging.info('done!')

if __name__ == '__main__':
    run()