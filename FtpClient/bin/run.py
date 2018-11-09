import sys
import os
import socketserver

cwd = os.getcwd()
parwd = os.path.dirname(cwd)
sys.path.append(parwd)

import core.ftpserverhandler as fh

ftpserver = socketserver.ThreadingTCPServer(('127.0.0.1',8080),fh.FtpServerHandler)
ftpserver.serve_forever()