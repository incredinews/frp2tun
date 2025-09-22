from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import requests
#import dns.resolver
import os
from pprint import pprint
import json

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        #self.send_header("Set-Cookie", "foo=bar")
        self.end_headers()
        #self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))
    def _set_response_err(self,msg: str):
        self.send_response(401)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        outmsg="<html><body><h1>"+msg+"</h1></body></html>"
        self.wfile.write(outmsg.encode('utf-8'))
    def _set_response_code(self,code: int):
        self.send_response(code)
        #self.send_header('Content-type', 'text/html')
        #self.end_headers()
        #return false;

    def do_GET(self):
        extips=os.environ.get('EXTIPS', "::1|127.0.0.1").split("|")
        if self.path.startswith("/favicon.ico"):
            self._set_response_code(404)
            return True
        if self.path.startswith("/ask") and self.path.startswith("/ask?domain="):
            #print("incoming "+self.path)
            mydomain=self.path.split("=")[1]
            #print("domain: "+mydomain)
            if "." in mydomain and len(mydomain)>3:
                dohurl = 'https://cloudflare-dns.com/dns-query'
                dnsanswers=[]
                client = requests.session()
                ip_valid=False
                err_found=False
                for mytype in ["A","AAAA"]:
                    if not err_found:
                        #params = {
                        #    'name': mydomain,
                        #    'type': mytype,
                        #    'ct': 'application/dns-json',
                        #    'method' : "POST",
                        #}
                        dohurl="https://8.8.8.8/resolve?type="+mytype+"&name="+mydomain
                        #print(dohurl)
                        #ae = client.get(dohurl, params=params)
                        ae = client.get(dohurl)
                        #print(ae.json())
                        try:
                            jsonres=ae.json()
                            if "Answer" in jsonres:
                                dnsanswers.append(jsonres["Answer"])
                            #if not "Answer" in jsonres:
                            #    self._set_response_err("NO_ANSWER")
                            #else:
                            #    
                        except:
                            msg="dnserr_NO_JSON"
                            #err_found=True
                            print("error on "+mydomain +" : "+msg)
                            #print(ae.text)
                            #self._set_response_err(msg)
                            #return false
                foundips=[]
                if len(dnsanswers)==0:
                    self._set_response_err("NO_ANSWER|NXDOMAIN")
                else:
                    for answer in dnsanswers:
                        #print(json.dumps(answer))
                        for record in answer:
                            if "data" in record:
                                foundips.append(record["data"])
                        for record in answer:
                            if "data" in record:
                                if record["data"] in extips and not ( record["data"] == "::1" or record["data"]== "127.0.0.1"):
                                   extips.remove(record["data"])
                                   foundips.remove(record["data"])                                   
                if len(extips) == 0 and len(foundips) == 0 :
                    self._set_response()
                else:
                    msg="NO_IP_MATCH_FOR: "+mydomain+" external "+json.dumps(extips)+" current: "+json.dumps(foundips)
                    print(msg)
                    self._set_response_err(msg)
                return True

            else:
                msg="err_INVALID_DOMAIN"
                print("rejected "+mydomain +" "+msg)
                self._set_response_err(msg)
                return True
#            else:
#                ##nonexistent domain
#                print("rejected "+mydomain +" dnserr")
#                pprint(ae.json())
#                self._set_response_err()
#            
#            for extip in extips:
#                if ":" in extip:
#                   mytype="AAAA"
#                else:
#                   mytype="A"
#               
#                if(ae.status_code==200):
#                    resjson=ae.json()
#                    print(resjson["Answer"])
#                    self._set_response()
        else:
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
            print(self.path)
            self._set_response()
            #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

#    def do_POST(self):
#        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
#        post_data = self.rfile.read(content_length) # <--- Gets the data itself
#        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
#                str(self.path), str(self.headers), post_data.decode('utf-8'))
#
#        self._set_response()
#        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=6790):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
