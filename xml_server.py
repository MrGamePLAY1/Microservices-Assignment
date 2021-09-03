from xmlrpc.server import SimpleXMLRPCServer

def wipeThePc(pcNumber):
    # wiping the pc
    return 'pc is now wiped'


def temp(sample):
    r = ''
    if sample < 10 or sample == 0:
        r = 'is cold'
    if sample > 10 or sample == 20:
        r = 'is warm'
    return r


server = SimpleXMLRPCServer(("localhost", 8001))
print("Listening on port 8001...")

server.register_function(temp, "temp")


server.serve_forever()
