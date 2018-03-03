from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import os
import shutil

def savefile(fname, messagecontent):
    os.chdir('files\\subs')
    with open(fname, 'wb') as ufl:
        ufl.write(messagecontent)
        ufl.close()
    os.chdir('..\\..')
    print "File saved!"

def escape(input):
    js_replacements = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;',
                       "'": '&#39;', '/': '&#x2F;', '`': '&#x60;', '=': '&#x3D;'}
    sanit = ''
    for char in input:
        if char in ['&', '<', '>', '"', "'", '/', '`', '=']:
            char = js_replacements[char]
        sanit += char

    return sanit

def downloads_ls():
    os.chdir('files\\repo')
    lsa = os.listdir(os.getcwd())
    os.chdir('..\\..')
    return lsa

def fetch(toFetch):
    global fetchpath
    fetchpath = str(toFetch)

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/upload"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><title>Submit a new file</title>"
            output += "<body>"
            output += "<h2> How's it going?</h2>"
            output += '''<form method = 'POST' enctype='multipart/form-data' action='/upload'> What file would you like to upload? </h2>
            <br><input name = 'filename' type = 'text' maxlength="40"><br> <input name = 'userfile' type = 'file'><br> <input type = 'submit' value = 'Upload'></form>'''
            output += "</body></html>"
            self.wfile.write(output.encode(encoding='utf_8'))
            return
        elif self.path.endswith("/download"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ready = downloads_ls()
            print ready
            output = ""
            output += "<html><title>Download an existing file</title>"
            output += "<body>"
            output += "<h2> Choose a file:</h2>"
            for file in ready:
                output += "<p>" + str(file) + "</p>"
            output += "<form method = 'POST' enctype='multipart/form-data' action='/download'> What file would you like to download? </h2><input name = 'filename' type = 'text'> <input type = 'submit' value = 'Download'></form>"
            output += "</body></html>"
            self.wfile.write(output.encode(encoding='utf_8'))
            return
        elif self.path.endswith("/file-get"):
            os.chdir('files\\repo')
            with open(fetchpath, 'rb') as f:
                self.send_response(200)
                self.send_header("Content-Type", 'application/octet-stream')
                self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(fetchpath)))
                fs = os.fstat(f.fileno())
                self.send_header("Content-Length", str(fs.st_size))
                self.end_headers()
                shutil.copyfileobj(f, self.wfile)
                f.close()
            print "Download Successful"
            os.chdir('..\\..')
            return
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><title>Files for debate</title><body>"
            output += "<p>Welcome to this convenient site I made to upload debate files to!</p>"
            output += "<a href=upload>" + 'Submit a file to be uploaded' + "</a>"
            output += "<p><a href=download>" + 'Access files others have submitted' + "</a></p><br>"
            output += "Number of visitors: <br>"
            output += '''<a href="http://counter5nolixj34.onion/visits.php?id=a17336fc5c02f2444f699f53e6acc3cf"><img style="height:24px;width:auto;" src="http://counter5nolixj34.onion/counter.gif?id=a17336fc5c02f2444f699f53e6acc3cf&bg=000000&fg=FFFFFF&tr=0&unique=0&mode=0"></a>'''
            output += "</body></html>"
            self.wfile.write(output.encode(encoding='utf_8'))
            print "Home"
            return

    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if (ctype == 'multipart/form-data') and (self.path.endswith('/upload')):
                filework = True
                fields = cgi.parse_multipart(self.rfile, pdict)
                fname = fields.get('filename')
                print fname
                messagecontent = fields.get('userfile')
                if ('.inf' not in fname[0]) and ('.exe' not in fname[0]):
                    savefile(fname[0], messagecontent[0])
            elif (ctype == 'multipart/form-data') and (self.path.endswith('/download')):
                filework = True
                fields = cgi.parse_multipart(self.rfile, pdict)
                fname = fields.get('filename')
                print fname
                fetch(fname[0])
                output = ""
                output += "<html><head>"
                output += '<meta http-equiv="refresh" content="0; url=/file-get" />'
                output += "</head><body>"
                output += "</body></html>"
                self.wfile.write(output.encode(encoding="utf_8"))
            if (filework):
                print "File + return"
                output = ""
                output += "<html>"
                output += "<body><a href='/'> Home </a></p>"
                output += "</body></html>"
                self.wfile.write(output.encode(encoding="utf_8"))
        except:
            pass

def main():
    try:
        port = 8000
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port: 8000"
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
