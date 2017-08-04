from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler
from .url_parse import UrlParse

class HTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Handler that will be call by the DaemonServer to routes requests
    """

    routes = {'GET': {}, 'POST': {}, 'DELETE': {}}

    @staticmethod
    def get(route):
        """
        Decorator to add a route for the GET method
        The function will be called with one parameter of type HTTPRequestHandler

            @param route: route to be handle
            @type route: string
        """
        def mapping(func):
            HTTPRequestHandler.routes['GET'][UrlParse(route)] = func
            return func
        return mapping

    @staticmethod
    def post(route):
        """
        Decorator to add a route for the POST method
        The function will be called with one parameter of type HTTPRequestHandler

            @param route: route to be handle
            @type route: string
        """
        def mapping(func):
            HTTPRequestHandler.routes['POST'][UrlParse(route)] = func
            return func
        return mapping

    @staticmethod
    def delete(route):
        """
        Decorator to add a route for the DELETE method
        The function will be called with one parameter of type HTTPRequestHandler

            @param route: route to be handle
            @type route: string
        """
        def mapping(func):
            HTTPRequestHandler.routes['DELETE'][UrlParse(route)] = func
            return func
        return mapping

    def __match(self, request_method):
        """
        Private method allowing the handler to find the route corresponding
        to the request and execute the corresponding function

            @param request_method: the request method
        """
        func = self.__get_route(request_method, self.path)
        if func is not None:
            response = func(self)
            self.send_response(response.status_code)
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:9080')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.text.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def __get_route(self, request_method, path):
        """
        Private method allowing to get the function matching the route from
        the request

            @param request_method: the request method
            @param path: the url requested
        """
        routes_method = self.routes[request_method]
        for route in routes_method:
            if route == path:
                self.url_vars = route.get_url_var(path)
                return routes_method[route]
        return None

    def do_OPTIONS(self):
        self.send_response(200, 'ok')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:9080')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Access-Control-Allow-Headers', 'Content-type')
        self.send_header('Access-Control-Allow-Headers', 'access-control-allow-origin')

    def do_GET(self):
        """
        Override the do_GET function from the BaseHTTPRequestHandler
        Handle the GET method
        """
        self.__match('GET')

    def do_POST(self):
        """
        Override the do_POST function from the BaseHTTPRequestHandler
        Handle the POST method
        """
        content_length = int(self.headers.get('content-length'))
        data = self.rfile.read(content_length).decode('utf-8')
        self.fields = parse_qs(data)
        self.__match('POST')

    def do_DELETE(self):
        """
        Handle the DELETE method
        """
        self.__match('DELETE')
