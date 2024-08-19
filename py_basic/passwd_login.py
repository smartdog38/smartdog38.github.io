import wx
from socket import socket,AF_INET,SOCK_STREAM
import time
import threading

#定义类------------------------------------------------------------------------------------------------------------------
class client_box(wx.Frame):
    def __init__(self):
        #定义------------------------------------------------------------------------------------------------------------
        #定义登录状态
        self.logged_in = False
        #定义服务器IP地址与端口
        self.server_host_port = ('127.0.0.1',8888)
        #定义注册状态
        self.sign_cond = False
        self.server_cond = False
        #绘制框架（DONE）--------------------------------------------------------------------------------------------------
        wx.Frame.__init__(self,None,id=1111,title='英雄系统',pos=wx.DefaultPosition,size=(550,600))
        pl = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        username_label = wx.StaticText(pl, label='用户名:')
        self.user_text = wx.TextCtrl(pl,size=(400,25))
        password_label = wx.StaticText(pl, label='密码:')
        self.passwd_text = wx.TextCtrl(pl, size=(400,25), style=wx.TE_PROCESS_ENTER | wx.TE_PASSWORD)
        box.Add(username_label, 0, wx.ALL | wx.LEFT, 10)
        box.Add(self.user_text,0,wx.ALL|wx.ALIGN_CENTRE,10)
        box.Add(password_label, 0, wx.ALL | wx.LEFT, 10)
        box.Add(self.passwd_text, 0,wx.ALL| wx.ALIGN_CENTRE,10)
        sign_in_btn = wx.Button(pl,size=(150,30),label='注册')
        log_in_btn = wx.Button(pl,size=(150,30),label='登录')
        pp = wx.FlexGridSizer(wx.HSCROLL)
        pp.Add(sign_in_btn,1)
        pp.Add(log_in_btn,1)
        box.Add(pp,1,wx.ALIGN_CENTRE,10)
        self.order_text = wx.TextCtrl(pl,size=(500,60),style = wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        self.answer_text = wx.TextCtrl(pl,size=(500,240),style=wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(self.order_text,0,wx.ALIGN_CENTRE|wx.ALL,10)
        box.Add(self.answer_text,0,wx.ALIGN_CENTRE|wx.ALL,10)
        pl.SetSizer(box)
        #绑定事件（DONE）--------------------------------------------------------------------------------------------------
        self.passwd_text.Bind(wx.EVT_TEXT_ENTER, self.Enter_log_in)#密码行回车登录
        self.order_text.Bind(wx.EVT_TEXT_ENTER, self.Enter_order)#命令行输入指令
        self.Bind(wx.EVT_BUTTON,self.sign_user,sign_in_btn)#注册事件
        self.Bind(wx.EVT_BUTTON, self.log_in, log_in_btn)#点击登录事件
        # 连接到服务器----------------------------------------------------------------------------------------------------
        self.client_socket = socket(AF_INET,SOCK_STREAM)
        self.client_socket.connect((self.server_host_port))
        self.answer_text.AppendText(time.strftime('%Y-%m-%d %H:%M-%S',time.localtime()) + "\n" + "已连接到服务器")
        self.server_cond = True
        self.recv_thread = threading.Thread(target=self.recv_message_thread)
        self.recv_thread.daemon = True
        self.recv_thread.start()
    #定义事件-------------------------------------------------------------------------------------------------------------
    #点击登录事件（done）
    def log_in(self,event):
        #找到用户名，密码，发给服务端
        if self.server_cond:
            if not self.sign_cond:
                if not self.logged_in:
                    self.send_message("login")
                    user_name = self.user_text.GetValue()
                    passwd = self.passwd_text.GetValue()
                    self.send_message(user_name)
                    self.send_message(passwd)
                else:
                    self.answer_text.Clear()
                    self.answer_text.AppendText("已经登录了！")
            else:
                self.answer_text.Clear()
                self.answer_text.AppendText("正在注册状态！")
        else:
            self.answer_text.Clear()
            self.answer_text.AppendText("服务已关闭！")
    #密码行回车登录事件（done）
    def Enter_log_in(self,event):
        #找到用户名，密码，发给服务端
        if self.server_cond:
            if not self.sign_cond:
                if not self.logged_in:
                    self.send_message("login")
                    user_name = self.user_text.GetValue()
                    passwd = self.passwd_text.GetValue()
                    self.answer_text.Clear()
                    self.send_message(user_name)
                    self.send_message(passwd)
                else:
                    self.answer_text.Clear()
                    self.answer_text.AppendText("已经登录了！")
            else:
                self.answer_text.Clear()
                self.answer_text.AppendText("正在注册状态！")
        else:
            self.answer_text.Clear()
            self.answer_text.AppendText("服务已关闭！")
    #指令行回车发送消息事件（done）
    def Enter_order(self, event):
        if self.server_cond:
            data = self.order_text.GetValue()
            self.send_message(data)
            self.order_text.Clear()
        else:
            self.answer_text.AppendText("服务已关闭")
    #注册用户（done）
    def sign_user(self,event):
        if self.server_cond:
            if not self.logged_in:
                self.sign_cond = True
                self.send_message("sign")
    #定义一些就函数，简便程序------------------------------------------------------------------------------------------------
    #发消息
    def send_message(self,data):
        self.client_socket.send(data.encode('utf-8'))
    #收信息线程，只显示最新消息
    def recv_message_thread(self):
        while True:
            data = self.client_socket.recv(1024).decode('utf-8')
            self.answer_text.Clear()
            if data == 'exit-c':
                self.answer_text.AppendText("已退出登录！")
                self.logged_in = False
            elif data == 'exit-s':
                self.send_message('exit-c')
            elif data == 'shutdown':
                self.answer_text.AppendText("服务已关闭！")
                self.server_cond = False
                self.client_socket.close()
                break
            elif data == 'logged':
                self.logged_in = True
            elif data == 'signned':
                self.answer_text.AppendText("用户已创建！")
                self.sign_cond = False
            else:
                self.answer_text.AppendText(data)



#--------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App()
    user = client_box()
    user.Show()
    app.MainLoop()