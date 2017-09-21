"""
@author: 黄帅
@contact: shuai.huang.iot@foxmail.com
@file: netMonitor.py
@time: 2017/9/21 上午9:30
@desc:

"""
import getopt
import time
import requests
import sys


class Monitor(object):
    def __init__(self, argv):
        self.Log = True
        self.net_enable = False
        self.username = ''
        self.password = ''

        try:
            opts, args = getopt.getopt(argv, "hu:p:l:", ["username=", "password=", "log="])
        except getopt.GetoptError:
            print('netMonitor.py -u <username> -p <password> -l<isLog>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('netMonitor.py -u <username> -p <password> -l<isLog>')
                sys.exit()
            elif opt in ("-u", "--username"):
                self.username = arg
            elif opt in ("-p", "--password"):
                self.password = arg
            elif opt in ("-l", "--log"):
                self.Log = True if arg == 'True' else False
        if self.username == '' or self.password == '':
            print('netMonitor.py -u <username> -p <password> -l<isLog>')
            sys.exit(2)
        self.main()

    def main(self):
        """
        通过百度的响应时间来判断网络连接状态
        :return:
        """
        print('校园网状态监控中...')
        while True:
            try:
                requests.get('https://www.baidu.com/', timeout=0.5)
                self.net_enable = True
                self.print_log()
            except:
                self.net_enable = False
                self.print_log()
                self.reconnect()

            time.sleep(1)

    def print_log(self):
        if self.Log:
            msg = '可联网' if self.net_enable else '不可联网'
            print(msg)

    def reconnect(self):
        """
        先进行注销登录操作，再重新登录
        :return:
        """
        print('断网重连...')
        # disConnect
        try:
            headers = {'Cookie': 'myusername=%s' % self.username}
            r = requests.get('http://172.16.200.11/F.htm', timeout=1, headers=headers)
        except:
            pass

        # connect
        headers = {'Content-Type': 'text/html; charset=gb2312;'}
        data = {'DDDDD': self.username, 'upass': self.password, '0MKKey': '登 录'}
        r = requests.post('http://172.16.200.11', timeout=1, headers=headers, data=data)
        print('断网重连成功...')


if __name__ == '__main__':
    Monitor(sys.argv[1:])
