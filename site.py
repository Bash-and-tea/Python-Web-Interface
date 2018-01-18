from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import os
import wget

def savefile(fname, messagecontent):
    sub_dir = os.path.normpath(os.path.join(os.path.expanduser('~'), 'Desktop/Web_dev/files/subs'))
    os.chdir(sub_dir)
    with open(fname, 'wb') as ufl:
        ufl.write(messagecontent)
        ufl.close()
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
    repo_dir = os.path.normpath(os.path.join(os.path.expanduser('~'), 'Desktop/Web_dev/files/repo'))
    os.chdir(repo_dir)
    lsa = os.listdir(os.getcwd())
    return lsa

def filedownload(fnme):
    home = os.path.expanduser('~')
    downpath = home + '\Downloads'
    os.chdir(downpath)
    src = 'file:///Users/Isaac/Desktop/Web_dev/files/repo/' + str(fnme)
    wget.download(src)

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
            <br><input name = 'filename' type = 'text'><br> <input name = 'userfile' type = 'file'><br> <input type = 'submit' value = 'Upload'></form>'''
            output += "</body></html>"
            self.wfile.write(output.encode(encoding='utf_8'))
            print output
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
            print output
            return
        elif self.path.endswith("/chatroom"):
            print "Chatting"
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h2> How's it going?</h2>"
            output += "<form method = 'POST' enctype='multipart/form-data' action='/chatroom'> What would you like me to say?</h2><input name = 'message' type = 'text'> <input type = 'submit' value = 'Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output.encode(encoding='utf_8'))
            return
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><title>Files for debate</title><body>"
            output += "<p>Welcome to this convenient site I made to upload debate files to!</p>"
            output += "<a href=upload>" + 'Submit a file to be uploaded' + "</a>"
            output += "<p><a href=download>" + 'Access files others have submitted' + "</a></p>"
            output += "<p><a href=chatroom> Join the chatroom </a></p>"
            output += "</body></html>"
            self.wfile.write(output.encode(encoding='utf_8'))
            print output
            return

    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if (ctype == 'multipart/form-data') and (self.path.endswith('/upload')):
                filework = False
                fields = cgi.parse_multipart(self.rfile, pdict)
                fname = fields.get('filename')
                print fname
                messagecontent = fields.get('userfile')
                if ('.inf' not in fname[0]) and ('.exe' not in fname[0]):
                    savefile(fname[0], messagecontent[0])
            elif (ctype == 'multipart/form-data') and (self.path.endswith('/download')):
                filework = False
                fields = cgi.parse_multipart(self.rfile, pdict)
                fname = fields.get('filename')
                print fname
                filedownload(fname[0])
            elif (ctype == 'multipart/form-data') and (self.path.endswith('/chatroom')):
                filework = True
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                echo = escape(messagecontent[0])
                output += "<h1> %s </h1>" % echo
                output += '''<form method='POST' enctype='multipart/form-data' action='/chatroom'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode(encoding="utf_8"))
            if (not filework):
                print "File return"
                output = ""
                output += "<html><body>"
                output += " <h2> What now?: </h2>"
                output += "<a href=/> Home </a>"
                output += "</body></html>"
                self.wfile.write(output.encode(encoding="utf_8"))
                print output
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
