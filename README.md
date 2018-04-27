# thrift 远程调用框架 RPC 

使用 java 程序 远程调用 python 程序

1. 使用 Maven 建立 Java 项目 

pom.xml:

		<!-- Thrift -->
		<dependency>
			<groupId>org.apache.thrift</groupId>
			<artifactId>libthrift</artifactId>
			<version>0.10.0</version>
		</dependency>
		<dependency>
			<groupId>org.slf4j</groupId>
			<artifactId>slf4j-log4j12</artifactId>
			<version>1.7.5</version>
		</dependency>


2. 再制定目录编写 thrift 接口


Hello.thrift:

'''
    namespace java service.demo
  
    service Hello {
        string helloString(1:string para)
    }
'''

运行命令：

thrift -r -gen py Hello.thrift

生成：
	gen-py
		-service
			-demo
				-Hello.java

thrift -r -gen java hello.thrift

	gen-java
		-Hello		__init__.py	logger.log	server.py
			-Hello-remote	Hello.py	Hello.pyc	__init__.py	__init__.pyc	constants.py	constants.pyc	ttypes.py	ttypes.pyc



3. 客户端

HelloServiceClient.java:

'''
import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;

public class HelloServiceClient {
	public static void main(String[] args) {
        System.out.println("客户端启动....");
        TTransport transport = null;
        try {
            transport = new TSocket("127.0.0.1", 9090);// 本地ip使用127.0.0.1，不然会出现 connection refused
            // 协议要和服务端一致
            TProtocol protocol = new TBinaryProtocol(transport);
            Hello.Client client = new Hello.Client(protocol);
            transport.open();
            String result = client.helloString("哈哈");// 调用定义的方法，并接受返回值
            System.out.println(result);
        } catch (TTransportException e) {
            e.printStackTrace();
        } catch (TException e) {
            e.printStackTrace();
        } finally {
            if (null != transport) {
                transport.close();
            }
        }
    }
}
'''	

同时将 生成的 Hello.java 文件放在和 HelloServiceClient.java 同一路径下。

4. 服务端

server.py

'''
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
'''