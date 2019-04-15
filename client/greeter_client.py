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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import os
import grpc
import logging
import subprocess

import helloworld_pb2
import helloworld_pb2_grpc


def run():
    channel = grpc.insecure_channel(os.environ.get("ADDRESS"))
    for i in range(1000):
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        if True:
            response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
            if i % 200 in [0, 1]:
                logging.info("Greeter client received: '%s'", response.message)
            if i == 577:
                my_pid = os.getpid()
                cmd = 'ls -l /proc/{}/fd'.format(my_pid)
                logging.info("Running command: %r", cmd)
                subprocess.check_call(cmd, shell=True)


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
    run()
