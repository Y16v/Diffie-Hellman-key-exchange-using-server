import socket as sock
import time


class Server:

    def __init__(self, port=8080):
        self.socket = sock.socket()
        self.host = ""
        self.port = port
        self._dir = "../app/src"

    def run_server(self):
        print("Run server on host", self.host, ":", self.port)
        self.socket.bind((self.host, self.port))

        self._waiting_connection()

    def _generate_status_line(self, code):
        if code == 200:
            status_line = "HTTP/1.1 200 OK\n"

        elif code == 404:
            status_line = "HTTP/1.1 404 Not Found\n"

        elif code == 501:
            status_line = "HTTP/1.1 501 Not Implemented\n"
        else:
            status_line = "HTTP/1.1 437 Unavailable for several reasons\n"
        return status_line

    def _generate_header(self, code):
        header = self._generate_status_line(code)
        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += "Date:" + current_date + "\n"\
                  "Server: Simple-Python-HTTP-Server\n" \
                  "Connection: close\n\n"
        return header.encode()

    def _get_method_response(self, request_method, file_requested):
        if file_requested == "/" or file_requested == "/index.html":
            file_requested = "/index.html"
        else:
            file_requested = "/registration.html"
        file_requested = self._dir + file_requested

        try:
            file_handler = open(file_requested, "rb")
            resource = file_handler.read()
            response_header = self._generate_header(200)
            file_handler.close()
        except Exception as ex:
            print("Cannot find requested resource", ex.args[0])
            response_header = self._generate_header(404)
            resource = b"<html>" \
                       b"<head>" \
                       b"<title>404</title>" \
                       b"</head>" \
                       b"<body>" \
                       b"<h1>404 Not Found</h1>" \
                       b"</body>" \
                       b"</html>"

        if request_method == "GET":
            response = response_header + resource
        else:
            response = response_header
        return response

    def _html_dict(self, dictionary):
        result = ""
        for k, v in dictionary.items():
            result += "<h3>{0}: {1}</h3>".format(k, v)

        return result.encode()

    def _post_method_request(self, entity_body):
        dictionary = {}
        entity_body = entity_body.split("&")
        for i in entity_body:
            key, val = i.split("=")
            dictionary[key] = val

        resource = b"<html>" \
                   b"<head>" \
                   b"<title> Successful </title>" \
                   b"</head>" \
                   b"<body>" + self._html_dict(dictionary) + \
                   b"</body>" \
                   b"</html>"

        response_header = self._generate_header(200)
        response = response_header + resource

        return response

    def _waiting_connection(self):
        while True:
            self.socket.listen(5)
            conn, adr = self.socket.accept()
            print("Connecting to adr:", adr)

            data = conn.recv(2048)

            request = data.decode()
            request = request.split()
            request_method, request_uri, http_version = request[:3]
            file_requested = request_uri.split("?")[0]
            if request_method == "GET" or request_method == "HEAD":
                response = self._get_method_response(request_method, file_requested)

                conn.send(response)

            elif request_method == "POST":
                entity_body = request[-1]
                response = self._post_method_request(entity_body)

                conn.send(response)

            conn.close()


server = Server(8080)
server.run_server()
