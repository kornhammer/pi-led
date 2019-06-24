#!/usr/bin/python3

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import json
from multiprocessing import Process
import asyncio


from lib.knight_rider import KnightRider

import time

hostName = ""
hostPort = 8080


class PiServer(BaseHTTPRequestHandler):

    tasks = []

    def camel(self, snake_str):
        first, *others = snake_str.split('_')
        return ''.join([first.capitalize(), *map(str.title, others)])

    def _set_headers(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    #	GET
    def do_GET(self):
        q = urllib.parse.parse_qs(self.path[2:])

        try:
            if ('action' in q):
                try:
                    action_id = self.camel(q['action'][0])
                    self.log_message("start led action: {{action_id}}")
                    constructor = globals()[action_id]
                    instance = constructor()
	            #task = asyncio.ensure_future(instance.run())
                    #self.tasks += task
                    instance.run()

                    self._set_headers(200)
                    self.wfile.write(json.dumps({
                        "msg": "success",
                        "action": action_id,
                        "error": False
                    }).encode("utf-8"))
                except Exception as ex:
                    self.log_error("error running led action")
                    print(ex)
                    self._set_headers(400)
                    self.wfile.write(json.dumps({
                        "msg": "could not load led action",
                        "action": action_id,
                        "error": True
                    }).encode("utf-8"))
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({
                    "msg": "led action param not found! Usage: ?action=q",
                    "error": True
                }).encode("utf-8"))
        except Exception as ex:
            self.log_error("unexpected exception")
            print(ex)
            self._set_headers(500)

    #	POST
    def do_POST(self):
        print("incomming http: ", self.path)

        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself
        post_data = self.rfile.read(content_length)
        self.send_response(200)

        client.close()

        # import pdb; pdb.set_trace()


piServer = HTTPServer((hostName, hostPort), PiServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(piServer)

    # Let's also cancel all running tasks:


    piServer.serve_forever()

    while 1:
        loop = asyncio.get_event_loop()
        # loop.run_until_complete(piServer.tasks)
        pending = asyncio.Task.all_tasks()
        print("pending", pending)
        for task in pending:
            task.cancel()
            # Now we should await task to execute it's cancellation.
            # Cancelled task raises asyncio.CancelledError that we can suppress:
            with suppress(asyncio.CancelledError):
                loop.run_until_complete(task)
        time.sleep(0.7)


except KeyboardInterrupt:
    pass

piServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
