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
        try:
            self.socket.bind((self.host, self.port))
        except Exception as ex:
            print("Exception:", ex.args[0])
            import sys
            sys.exit(1)
        self._waiting_connection()

    def _generate_status_line(self, code):
        if code == 200:
            status_line = "HTTP/1.1 200 OK\r\n"

        elif code == 303:
            status_line = "HTTP/1.1 303 See Other\r\n"

        elif code == 404:
            status_line = "HTTP/1.1 404 Not Found\r\n"

        elif code == 501:
            status_line = "HTTP/1.1 501 Not Implemented\r\n"
        else:
            status_line = "HTTP/1.1 437 Unavailable for several reasons\r\n"
        return status_line

    def _generate_header(self, code, location=""):
        header = self._generate_status_line(code)
        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        if code == 303:
            header += location

        header += "Date:" + current_date + "\r\n" \
                  "Server: Simple-Python-HTTP-Server\r\n" \
                  "Content-Type: text/html; charset=UTF-8\r\n" \
                  "Connection: keep-alive\r\n\r\n"

        return header.encode()

    def _get_method_response(self, request_method, file_requested):
        if file_requested == "/" or file_requested == "/index.html":
            file_requested = "/index.html"

        file_requested = self._dir + file_requested

        try:
            file_handler = open(file_requested, "rb")
            resource = file_handler.read()
            response_header = self._generate_header(200)
            file_handler.close()
        except Exception as ex:
            print("Cannot find requested resource", ex.args[0])
            resource = b"<html>" \
                       b"<head>" \
                       b"<title>404</title>" \
                       b"</head>" \
                       b"<body>" \
                       b"<h1>404 Not Found</h1>" \
                       b"</body>" \
                       b"</html>"

            response_header = self._generate_header(404)

        if request_method == "GET":
            response = response_header + resource
        else:
            response = response_header
        return response

    def _post_method_request(self):
        response_header = self._generate_header(303, "Location: /successful.html\r\n")

        return response_header

    def _waiting_connection(self):
        while True:
            self.socket.listen(5)
            conn, adr = self.socket.accept()
            print("Connecting to adr:", adr)

            data = conn.recv(4096)
            request = data.decode()
            request_method, request_uri, *request = request.split()
            file_requested = request_uri.split("?")[0]
            if request_method == "GET" or request_method == "HEAD":
                response = self._get_method_response(request_method, file_requested)

            elif request_method == "POST":
                response = self._post_method_request()
            else:
                response = self._generate_header(437)
            conn.send(response)

            conn.close()


server = Server(8080)
server.run_server()
