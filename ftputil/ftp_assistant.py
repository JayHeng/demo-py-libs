import sys, os
import ftputil

class ftpAssistant(object):

    def __init__(self, ip, port, user, passwd):
        self.ftp = ftputil.FTPHost(ip, user, passwd)

    def createDirectory(self, dirPath):
        if not self.ftp.path.isdir(dirPath):
            self.ftp.makedirs(dirPath)

    def deleteDirectory(self, dirPath):
        if self.ftp.path.isdir(dirPath):
            self.ftp.rmtree(dirPath)
        elif self.ftp.path.isfile(dirPath):
            self.ftp.remove(dirPath)
        else:
            pass

    def downloadFile(self, remoteFile, localPath, newFileName):
        if self.ftp.path.isfile(remoteFile):
            if newFileName == None:
                remoteDirPath, remoteBasename = os.path.split(remoteFile)
                localFile = localPath + '\\' + remoteBasename
            else:
                localFile = localPath + '\\' + newFileName
            self.ftp.download(remoteFile, localFile)

    def uploadFile(self, localFile, remotePath, newFileName):
        if os.path.isfile(localFile):
            self.createDirectory(remotePath)
            if newFileName == None:
                localDirname, localBasename = os.path.split(localFile)
                remoteFile = remotePath + '/' + localBasename
            else:
                remoteFile = remotePath + '/' + newFileName
            self.ftp.upload(localFile, remoteFile)

    def __del__( self ):
        pass

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

