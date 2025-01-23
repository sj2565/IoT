from http.server import HTTPServer, SimpleHTTPRequestHandler

class SensorHttpHandler(SimpleHTTPRequestHandler):
      def do_GET(self):            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = '<html><head><meta http-equiv="Content="text/html" charset="UTF-8">'
            output += '<title>My Web Server</title></head>'
            output += '<body>'
            output += '<p>Request: %s</p>' % (self.path)
            output += '<p>저장된 데이터 개수 : %d </p>' % (self.server.gateway.countDbVolt())
            output += self.server.gateway.makeHtmlTableVolt()
            output += '</body></html>'
            self.wfile.write(output.encode())