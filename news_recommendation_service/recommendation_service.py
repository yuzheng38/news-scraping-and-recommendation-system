import operator
import os
import pyjsonrpc
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

PREFERENCE_MODEL_TABLE_NAME = 'user_preference_model'

SERVER_HOST = 'localhost'
SERVER_PORT = 5050

# python implementation of approximate equality: https://www.python.org/dev/peps/pep-0485/#proposed-implementation
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

# request handler for rpc server
class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """ Get user's preference """ 
    @pyjsonrpc.rpcmethod
    def getPreferenceForUser(self, user_id):
        db = mongodb_client.get_db()
        model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': user_id})
        if model is None:
            return []

        sorted_tuples = sorted(model['preference'].items(), key=operator.itemgetter(1), reverse=True)
        sorted_list = [x[0] for x in sorted_tuples]
        sorted_value_list = [x[1] for x in sorted_tuples]

        if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
            return []

        return sorted_list

# start the server. 
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()