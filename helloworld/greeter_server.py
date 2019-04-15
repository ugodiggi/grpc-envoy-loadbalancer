# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging
import os
import time

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        message = 'Hello, %s from host=%s!' % (request.name, os.environ.get("HOSTNAME", "Unknown"))
        logging.info('Received SayHello request, will respond with %r', message)
        return helloworld_pb2.HelloReply(message=message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def _init_logging():
    DATE_FMT = '%Y%m%d %H:%M:%S'
    FORMAT = (
      '%(levelname).1s'  # A single char for the log level ('I', 'W', 'E')
      '%(asctime)s '  # timestamp printed according to DATE_FMT
      '%(filename)s:%(lineno)d '  # the name, line number of the log statement
      '%(message).10000s' # the log message, limited to 10000 characters for sanity.
    )
    logging.basicConfig(format=FORMAT, datefmt=DATE_FMT, level='INFO')


if __name__ == '__main__':
    _init_logging()
    serve()
