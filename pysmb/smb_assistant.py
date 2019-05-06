
# Library Name:  pysmb
# Main Page:     https://miketeo.net/wp/index.php/projects/pysmb
# Download:      https://pypi.org/project/pysmb/
# Documentation: https://pysmb.readthedocs.io/en/latest/

import sys, os
from smb.SMBConnection import SMBConnection

class smbAssistant(object):

    def __init__(self, ip, port, user, passwd, server):
        self.samba = SMBConnection(user, passwd, 'Any', "MCUSW-BUILD-09", use_ntlm_v2 = True)
        assert self.samba.connect(ip, port)
        self.server = server

    def createDirectory(self, dirPath):
        self.samba.createDirectory(self.server, dirPath, timeout=30)

    def deleteDirectory(self, dirPath):
        pass

    def downloadFile(self, remoteFile, localPath, newFileName):
        if newFileName == None:
            remoteDirPath, remoteBasename = os.path.split(remoteFile)
            localFile = localPath + '\\' + remoteBasename
        else:
            localFile = localPath + '\\' + newFileName
        fileObj = open(localFile, 'w')
        self.samba.retrieveFile(self.server, remoteFile, fileObj)
        fileObj.close()

    def uploadFile(self, localFile, remotePath, newFileName):
        if newFileName == None:
            localDirname, localBasename = os.path.split(localFile)
            remoteFile = remotePath + '/' + localBasename
        else:
            remoteFile = remotePath + '/' + newFileName
        fileObj = open(localFile, 'rb')
        self.samba.storeFile(self.server, remoteFile, fileObj)
        fileObj.close()

    def __del__( self ):
        pass

def main(argv=None):
    localDirPath = os.path.abspath(os.path.dirname(__file__))
    localFilename = 'smb_data_local.bin'
    localFile = os.path.join(localDirPath, localFilename)
    fileObj = open(localFile, "wb")
    fileObj.write('1234567')
    fileObj.close()

    mySmb = smbAssistant("10.193.108.156", 139, "anonynous", "Qwer!234", "packages")
    remoteDirPath = '/smb_test/'

    remoteFilename = 'smb_data_remote.bin'
    remoteFile = remoteDirPath + remoteFilename

    mySmb.createDirectory(remoteDirPath)
    mySmb.uploadFile(localFile, remoteDirPath, remoteFilename)
    mySmb.downloadFile(remoteFile, localDirPath, None)

if __name__ == "__main__":
    sys.exit(main())

