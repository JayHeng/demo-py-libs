
# Library Name:  pycurl
# Main Page:     http://pycurl.io/
# Download:      https://pypi.org/project/pycurl/
# Documentation: http://pycurl.io/docs/latest/index.html
#                http://pycurl.io/docs/latest/curlobject.html
#                https://curl.haxx.se/libcurl/c/curl_easy_setopt.html

import sys, os
import pycurl
from cStringIO import StringIO

class curlAssistant(object):

    def __init__(self, url, user, passwd ):
        self.curl = pycurl.Curl()
        self.curl.setopt(self.curl.URL, url)
        #####################################
        # Fix error: 301 Moved Permanently
        #            The document has moved <a href="http://zcz09fs.ea.freescale.net/mcux_sdk_builds/squashes/">here
        #####################################
        self.curl.setopt(self.curl.FOLLOWLOCATION, True)
        #self.curl.setopt(c.PORT, 80)
        self.curl.setopt(self.curl.USERNAME, user)
        self.curl.setopt(self.curl.PASSWORD, passwd)

    def createDirectory(self, dirPath):
        pass

    def deleteDirectory(self, dirPath):
        pass

    def downloadFileGet(self, filename ):
        fileObj = open(filename, 'wb')
        self.curl.setopt(self.curl.WRITEDATA, fileObj)
        self.curl.perform()
        fileObj.close()

    def uploadFileFtpput(self, localFile ):
        self.curl.setopt(self.curl.UPLOAD, 1)
        fileObj = open(localFile, 'rb')
        self.curl.setopt(self.curl.READDATA, fileObj)
        self.curl.perform()
        fileObj.close()

    def uploadFileFtpput2(self, localFile ):
        self.curl.setopt(self.curl.UPLOAD, 1)
        fileObj = open(localFile, 'rb')
        self.curl.setopt(self.curl.READFUNCTION, fileObj.read)
        self.curl.setopt(self.curl.INFILESIZE, os.path.getsize(localFile))
        self.curl.perform()
        fileObj.close()

    def uploadFileHttppost(self, localFile ):
        newLocalFile = ''
        for i in range(len(localFile)):
            newLocalFile += localFile[i]
            if localFile[i] == '\\':
                newLocalFile += '\\'
        self.curl.setopt(self.curl.POST, 1)
        self.curl.setopt(self.curl.HTTPPOST, [
            ('fileUpload', (
                self.curl.FORM_FILE, newLocalFile,
            )),
        ])
        self.curl.perform()

    def uploadFileHttppost2(self, localFile ):
        newLocalFile = ''
        for i in range(len(localFile)):
            newLocalFile += localFile[i]
            if localFile[i] == '\\':
                newLocalFile += '\\'
        #self.curl.setopt(self.curl.POST, 1)
        self.curl.setopt(self.curl.HTTPPOST, [
            ('fileUpload', (
                self.curl.FORM_FILE, newLocalFile,
            )),
        ])
        #self.curl.setopt(self.curl.VERBOSE, 1)
        bodyOutput = StringIO()
        headersOutput = StringIO()
        self.curl.setopt(self.curl.WRITEFUNCTION, bodyOutput.write)
        self.curl.setopt(self.curl.HEADERFUNCTION, headersOutput.write)
        self.curl.perform()

    def __del__( self ):
        self.curl.close()

def main(argv=None):
    localDirPath = os.path.abspath(os.path.dirname(__file__))
    localFilename = 'curl_data_local.bin'
    localFile = os.path.join(localDirPath, localFilename)
    fileObj = open(localFile, "wb")
    fileObj.write('1234567')
    fileObj.close()

    remoteFilename = 'curl_data_remote.bin'

    #-------------------------------------------------------------------------------------
    # Use FTP protocol
    myCurl = curlAssistant('ftp://zcz09fs.ea.freescale.net/mcux_sdk_builds/squashes/' + remoteFilename, 'mcux_sdk_builds', 'mcux_sdk_builds')
    #myCurl.uploadFileFtpput(localFile)
#    myCurl.uploadFileFtpput2(localFile)
    myCurl.downloadFileGet(remoteFilename)

    #-------------------------------------------------------------------------------------
    # Switch to HTTP protocol
    #myCurl = curlAssistant('http://zcz09fs.ea.freescale.net/mcux_sdk_builds/squashes/', 'mcux_sdk_builds', 'mcux_sdk_builds')
    #####################################
    # Fix HTTP error: 404 Not Found
    #                The requested URL /mcux_sdk_builds/squashes/ was not found on this server.
    #####################################
#    myCurl = curlAssistant('http://zcz09fs.ea.freescale.net/mcux_sdk_builds/squashes', 'mcux_sdk_builds', 'mcux_sdk_builds')
    #myCurl.uploadFileFtpput(localFile)
    #####################################
    # Fix HTTP error: 405 Method Not Allowed
    #                 The requested method PUT is not allowed for the URL /mcux_sdk_builds/squashes/
    #####################################
    # python console: Can see file info under url but cannot upload file
#    myCurl.uploadFileHttppost(localFile)
    # python console: Can see ip address of url and connection info but cannot upload file
#    myCurl.uploadFileHttppost2(localFile)

#    myCurl = curlAssistant('http://zcz09fs.ea.freescale.net/mcux_sdk_builds/squashes/' + remoteFilename, 'mcux_sdk_builds', 'mcux_sdk_builds')
#    myCurl.downloadFileGet(remoteFilename)

if __name__ == "__main__":
    sys.exit(main())

