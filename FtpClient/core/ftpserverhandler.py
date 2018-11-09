import socketserver
import os
import hmac
import json
import sys

cwd = os.getcwd()
parwd = os.path.dirname(cwd)
sys.path.append(parwd)

from core import filemanage

class FtpServerHandler(socketserver.BaseRequestHandler):
    flag_Login = False

    def handle(self):
        print('The conn is:', self.request)
        print('The addr is:', self.client_address)

        if not self.safety_test():
            self.request.close()
            print("illegal connection!")
            return None

        if not self.Login():
            self.request.close()
            print("fail to login!")
            return None

        print("Login success!")
        self.request.sendall("Login success!".encode('utf-8'))

        name = self.userdata['name']
        space = self.userdata['space']
        permission = self.userdata['Permission']
        self.controler = filemanage.CloudHandler(name,space,permission)

        while True:
            command = self.recv_msg()





    def safety_test(self):
        # 加盐检验安全链接
        secret_key = b'secret'  # 可以放到conf里
        digest_method = 'MD5'
        msg = os.urandom(32)
        self.request.sendall(msg)
        h = hmac.new(secret_key, msg, digestmod=digest_method)
        ha = h.digest()
        recv_ha = self.request.recv(len(ha))
        if hmac.compare_digest(ha, recv_ha):
            print('链接合法')
            return True
        else:
            print('链接不合法，关闭')
            return False

    def _get_accounts_data(self):# get the data of users'accounts
        cwd = os.getcwd()
        parwd = os.path.dirname(cwd)
        filename = os.path.join(parwd, 'conf', 'accounts.json')
        with open(filename, 'r', encoding='utf-8') as f:
            accounts_data = json.load(f)
            return accounts_data

    def send_msg(self,msg):
        self.request.sendall(msg.encode('utf-8'))

    def recv_msg(self):
        msg = self.request.recv(1024).decode('utf-8')
        return msg

    def Login(self):
        msg = 'Enter'  # tell the client that it successfully enter the login page
        self.send_msg(msg)

        accounts_data = self._get_accounts_data()
        print(accounts_data)
        # login
        username_times = 0 # The times client enter the wrong username
        password_times = 0  # The times client enter the wrong password
        while username_times<5 and password_times<=5:
            username = self.recv_msg()
            print(username)
            if username in accounts_data['users']:
            # if username =="admin":
                # correct username
                msg = 'Please enter your password'
                self.send_msg(msg)
                while password_times<=4:
                    password = self.recv_msg()
                    if password == accounts_data['data'][username]['pwd']:
                        self.flag_Login = True
                        # self.username = username
                        self.userdata = accounts_data['data'][username]
                        return True
                    else:
                        password_times+=1
                    msg = "Your password is not correct! It remain %d chances."%(5-password_times)
                    self.send_msg(msg)
            else:
                username_times +=1
                msg = "The user doesn't exist, you still have %d chances to try"%(5 - username_times)
                self.send_msg(msg)
        return False


if __name__ == "__main__":
    print('launch server!')
    ftpserver = socketserver.ThreadingTCPServer(('127.0.0.1',8080),FtpServerHandler)
    ftpserver.serve_forever()
