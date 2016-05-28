#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from hello import HelloHandler
from user import UserHandler
from callback import CallbackHandler

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("ip", default="127.0.0.1", help="run on the given ip", type=str)

def main():
    tornado.options.parse_config_file("./server.conf")
    #tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", HelloHandler),
        (r"/user", UserHandler),
        (r"/callback", CallbackHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    print("run on: %s port: %d" % (options.ip, options.port))
    main()
