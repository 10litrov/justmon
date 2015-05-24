import json
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.static import File


def jsonify(data):
    def handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))

    return json.dumps(data, separators=(',', ':'), default=handler)


class Api(Resource):
    isLeaf = True

    @staticmethod
    def sendJSON(data, request):
        request.setHeader('content-type', 'application/json; charset=UTF-8')
        request.write(jsonify(data))
        request.finish()

    @staticmethod
    def sendError(error, code, request):
        request.setResponseCode(code)
        request.setHeader('content-type', 'application/json; charset=UTF-8')
        request.write(jsonify({'error': str(error)}))
        request.finish()

    def send(self, deferred, request):
        deferred.addCallbacks(
            callback=self.sendJSON, callbackArgs=(request, ),
            errback=self.sendError, errbackArgs=(500, request)
        )

    def render_GET(self, request):
        path = next(iter(request.postpath), None)
        if path == 'hosts':
            self.send(request.site.db.getAllHostStatus(), request)
        else:
            self.sendError('No Such Resource', 404, request)

        return NOT_DONE_YET


class WebSite(Site):
    def __init__(self, db):
        root = Resource()
        root.putChild('api', Api())
        root.putChild('', File('./static'))
        
        Site.__init__(self, root)

        self.db = db
