from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

memory = []
form = '''<!DOCTYPE html>
    <title>Udacian</title>
    <form method="POST" action="http://localhost:8000/">
    <textarea name="name">name</textarea>
    <br>
    <textarea name="city">city</textarea>
    <br>
    <textarea name="enrollment">enrollment</textarea>
    <br>
    <textarea name="nanodegree">nanodegree</textarea>
    <br>
    <textarea name="status">status</textarea>
    <br>
    <button type="submit">Post it!</button>
    </form>
    <pre>
    {}
    </pre>   
'''


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # How long was the message?
        length = int(self.headers.get('Content-length', 0))

        # Read and parse the message
        data = self.rfile.read(length).decode()
        name = parse_qs(data)["name"][0]
        city = parse_qs(data)["city"][0]
        enrollment = parse_qs(data)['enrollment'][0]
        nanodegree = parse_qs(data)['nanodegree'][0]
        status = parse_qs(data)['status'][0]

        # Store it in memory.
        message =  name + '</br>' + city + '</br>' + enrollment + '</br>' + nanodegree + '</br>' + status

        memory.append(message)

        # Send a 303 back to the root page
        self.send_response(303)  # redirect via GET
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        # First, send a 200 OK response.
        self.send_response(200)

        # Then send headers.
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # Send the form with the messages in it.
        mesg = form.format("\n".join(memory))
        self.wfile.write(mesg.encode())


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()
