
# Library Name:  ftplib
# Main Page:     N/A
# Download:      N/A
# Documentation: https://docs.python.org/2/library/ftplib.html

import sys, os
from ftplib import FTP

class ftpAssistant(object):

    def __init__(self, ip, port, user, passwd):
        self.ftp = FTP()
        self.ftp.connect(ip, port)
        try:
            self.ftp.login(user, passwd)
            print(self.ftp.getwelcome())
        except:
            sys.exit()

    def createDirectory(self, dirPath):
        dirSplit = dirPath.split('/')
        curDir = ''
        # Create the directory level by level
        for i in range(len(dirSplit)):
            curDir += '/' + dirSplit[i]
            if dirSplit[i] != '':
                # Check to see whether the directory of current level exists
                try:
                    self.ftp.cwd(curDir)
                except:
                    # Current directory doesn't exist, then just create it
                    self.ftp.mkd(curDir)

    def deleteDirectory(self, dirPath):
        # Check to see whether dirPath is a valid directory
        try:
            self.ftp.cwd(dirPath)
        except:
            # dirPath is not a valid directory, then treat it as a file
            #  and try to delete it once.
            try:
                self.ftp.delete(dirPath)
            except:
                pass
            return
        # dirPath is a valid directory, get item(file,dir) list under dirPath
        dirList = self.ftp.nlst(dirPath)
        # Delete/Remove the item under dirPath in sequence
        for curDir in dirList:
            try:
                # Always treat curDir as a file first and try to delete it
                self.ftp.delete(curDir)
            except:
                # curDir is actually directory, call deleteDirectory() to remove it
                self.deleteDirectory(curDir)
        # Finally, we can remove the empty dirPath
        self.ftp.rmd(dirPath)

    def downloadFile(self, remoteFile, localPath, newFileName):
        remoteDirPath, remoteBasename = os.path.split(remoteFile)
        # Check to see whether remoteFile exists
        remoteDirList = self.ftp.nlst(remoteDirPath)
        hasRemoteFile = False
        for curDir in remoteDirList:
            if curDir == remoteFile:
                hasRemoteFile = True
                break
        if hasRemoteFile:
            # Specify localFile name
            if newFileName == None:
                localFile = localPath + '\\' + remoteBasename
            else:
                localFile = localPath + '\\' + newFileName
            # Download remoteFile from FTP server and save it to localFile
            fileObj = open(localFile, 'wb')
            self.ftp.retrbinary('RETR %s' %(remoteFile), fileObj.write, 4096)
            fileObj.close()

    def uploadFile(self, localFile, remotePath, newFileName):
        # Check to see whether localFile exists
        if os.path.isfile(localFile):
            # Try to create remote directory, in case it doesn't exist
            self.createDirectory(remotePath)
            # Specify remoteFile name
            if newFileName == None:
                localDirname, localBasename = os.path.split(localFile)
                remoteFile = remotePath + '/' + localBasename
            else:
                remoteFile = remotePath + '/' + newFileName
            # Upload localFile to FTP server and save it to remoteFile
            fileObj = open(localFile, "rb")
            self.ftp.storbinary('STOR %s' %(remoteFile), fileObj, 4096)
            fileObj.close()

    def __del__( self ):
        self.ftp.quit()

def main(argv=None):
    localDirPath = os.path.abspath(os.path.dirname(__file__))
    localFilename = 'ftp_data_local.bin'
    localFile = os.path.join(localDirPath, localFilename)
    fileObj = open(localFile, "wb")
    fileObj.write('1234567')
    fileObj.close()

    #myFtp = ftpAssistant("10.193.108.156", 21, "mcuxpresso", "mcuxpresso")
    #remoteDirPath = '/packages/ftp_test/test/'
    myFtp = ftpAssistant("92.120.196.100", 21, "nxa16738", "Welcome@123")
    remoteDirPath = '/ftp_test/test/'

    remoteFilename = 'ftp_data_remote.bin'
    remoteFile = remoteDirPath + remoteFilename

    myFtp.createDirectory(remoteDirPath)
    myFtp.uploadFile(localFile, remoteDirPath, remoteFilename)
    myFtp.downloadFile(remoteFile, localDirPath, None)
    myFtp.deleteDirectory(remoteDirPath)

if __name__ == "__main__":
    sys.exit(main())

