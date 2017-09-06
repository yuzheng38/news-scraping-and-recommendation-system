""" Backend python server """
import operations
import pyjsonrpc


SERVER_HOST = 'localhost'
SERVER_PORT = 4040

"""Request handler class to be used by pyjsonrpc"""

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    @pyjsonrpc.rpcmethod
    def add(self, first_num, second_num): #pylint: disable=no-self-use
        """ Test method """
        print 'add is called with %d and %d' % (first_num, second_num)
        return first_num + second_num

    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num):
        return operations.getNewsSummariesForUser(user_id, page_num)

    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self, user_id, news_id):
        return operations.logNewsClickForUser(user_id, news_id)

# Threading HTTP-Server
HTTP_SERVER = pyjsonrpc.ThreadingHttpServer(
    server_address=(SERVER_HOST, SERVER_PORT),
    RequestHandlerClass=RequestHandler
)

print "Starting Http server on %s:%d" % (SERVER_HOST, SERVER_PORT)

HTTP_SERVER.serve_forever()
