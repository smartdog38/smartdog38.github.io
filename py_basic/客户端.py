# import wx
from socket import socket,AF_INET,SOCK_STREAM
# import time
# from threading import Thread
# import openpyxl
#
#
# #导入xlsl-----------------------------------------------------------------------------------------------------------------
# work_book = openpyxl.load_workbook(r"C:\Users\smart dogs\Desktop\新建 XLSX 工作表.xlsx")#save
# work_sheet = work_book.active#找值
# #定义类------------------------------------------------------------------------------------------------------------------
# class Log_in(wx.Frame):
#     def __init__(self,work_book,work_sheet):
#         #定义------------------------------------------------------------------------------------------------------------
#         #定义登录状态
#         self.logged_in = False
#         #定义套接字
#         self.client_socket = None
#         #定义服务器IP地址与端口
#         self.server_host_port = ('127.0.0.1',8888)
#         #定义excel
#         self.work_sheet = work_sheet
#         self.work_book = work_book
#
# #绘制框架（DONE）----------------------------------------------------------------------------------------------------------
#         wx.Frame.__init__(self,None,id=1111,title='英雄系统Login',pos=wx.DefaultPosition,size=(550,600))
#         pl = wx.Panel(self)
#         box = wx.BoxSizer(wx.VERTICAL)
#         username_label = wx.StaticText(pl, label='用户名:')
#         self.user_text = wx.TextCtrl(pl,size=(400,25))
#         password_label = wx.StaticText(pl, label='密码:')
#         self.passwd_text = wx.TextCtrl(pl, size=(400,25), style=wx.TE_PROCESS_ENTER | wx.TE_PASSWORD)
#         box.Add(username_label, 0, wx.ALL | wx.LEFT, 10)
#         box.Add(self.user_text,0,wx.ALL|wx.ALIGN_CENTRE,10)
#         box.Add(password_label, 0, wx.ALL | wx.LEFT, 10)
#         box.Add(self.passwd_text, 0,wx.ALL| wx.ALIGN_CENTRE,10)
#         sign_in_btn = wx.Button(pl,size=(150,30),label='注册')
#         log_in_btn = wx.Button(pl,size=(150,30),label='登录')
#         pp = wx.FlexGridSizer(wx.HSCROLL)
#         pp.Add(sign_in_btn,1)
#         pp.Add(log_in_btn,1)
#         box.Add(pp,1,wx.ALIGN_CENTRE,10)
#         self.order_text = wx.TextCtrl(pl,size=(500,60),style = wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
#         self.answer_text = wx.TextCtrl(pl,size=(500,240),style=wx.TE_MULTILINE|wx.TE_READONLY)
#         box.Add(self.order_text,0,wx.ALIGN_CENTRE|wx.ALL,10)
#         box.Add(self.answer_text,0,wx.ALIGN_CENTRE|wx.ALL,10)
#         pl.SetSizer(box)
# #绑定事件（DONE）--------------------------------------------------------------------------------------------------------------
#
#         self.passwd_text.Bind(wx.EVT_TEXT_ENTER, self.Enter_log_in)#密码行回车登录
#         self.order_text.Bind(wx.EVT_TEXT_ENTER, self.send_to_server)#命令行输入指令
#         self.Bind(wx.EVT_BUTTON,self.sign_in,sign_in_btn)#注册
#         self.Bind(wx.EVT_BUTTON, self.log_in, log_in_btn)#登录
#
#
# #定义事件-----------------------------------------------------------------------------------------------------------------
#     #接受信息
#     def recv_data(self):
#         while self.isConnect:
#             data = self.client_socket.recv(1024).decode('utf-8')
#             self.answer_text.AppendText(data)
#
#     #回车发送信息
#     def send_to_server(self, event):
#         if self.isConnect:
#             data = self.order_text.GetValue()
#             if data != '':
#                 self.client_socket.send(data.encode('utf-8'))
#                 self.order_text.Clear()
#                 if data == 'exit':
#                     self.logged_in = False
#                     self.isConnect = False
#                     if self.client_socket:
#                         self.client_socket.close()
#         # if self.isConnect:   ???????????????????????????
#         #     data = self.order_text.GetValue()
#         #     if data != '':
#         #         self.order_text.Clear()
#         #         if data == 'exit':
#         #             self.logged_in = False
#         #             self.isConnect = False
#         #             if self.client_socket:
#         #                 self.client_socket.close()
#         #         else:
#         #             self.client_socket.send(data.encode('utf-8'))
#
#
#
#     def log(self):
#         if self.logged_in == False:
#             self.answer_text.Clear()
#             user_name = self.user_text.GetValue()
#             if user_name in self.user_dict.keys():
#                 passwd = self.passwd_text.GetValue()
#                 if passwd == self.user_dict[user_name]:
#                     self.logged_in = True
#                     self.answer_text.AppendText("登录成功！！！\n" + time.strftime('%Y-%m-%d  %H-%M-%S',time.localtime())+"\n正在连接服务器...\n")
#                     if self.isConnect == False:
#                         self.isConnect = True
#                         self.client_socket = socket(AF_INET,SOCK_STREAM)
#                         self.client_socket.connect(self.server_host_port)
#                         self.client_socket.send(user_name.encode('utf-8'))
#                         self.answer_text.AppendText("服务器连接成功！\n" + time.strftime('%Y-%m-%d  %H-%M-%S',time.localtime())+"\n\n\n")
#                         recv_thread = Thread(target=self.recv_data)
#                         # recv_thread.daemon = True
#                         recv_thread.start()
#                 else:
#                     self.answer_text.AppendText("密码错误！\n" + time.strftime('%Y-%m-%d  %H-%M-%S',time.localtime()))
#             else:
#                 self.answer_text.AppendText("该用户不存在！\n" + time.strftime('%Y-%m-%d  %H-%M-%S',time.localtime()))
#
#     #密码框的回车登录
#     def Enter_log_in(self,event):
#         self.log()
#
#     def log_in(self,event):
#         self.log()
#
#     #注册登录
#     def sign_in(self,event):
#         self.answer_text.Clear()
#         if self.logged_in == False:
#             user_name =self.user_text.GetValue()
#             if user_name in self.user_dict:
#                 self.answer_text.AppendText("用户名已存在！\n" + time.strftime('%Y-%m-%d  %H-%M-%S',time.localtime()))
#             else:
#                 self.user_dict[user_name] = self.passwd_text.GetValue()
#                 self.answer_text.AppendText("用户名已创建！\n" + time.strftime('%Y-%m-%d  %H-%M-%S',time.localtime())+"\n正在连接服务器...\n")
#                 if self.isConnect == False:
#                     self.isConnect = True
#                     self.client_socket = socket(AF_INET, SOCK_STREAM)
#                     self.client_socket.connect(self.server_host_port)
#                     self.client_socket.send(user_name.encode('utf-8'))
#                     self.answer_text.AppendText("服务器连接成功！\n" + time.strftime('%Y-%m-%d  %H-%M-%S',time.localtime())+"\n\n\n")
#                     recv_thread = Thread(target=self.recv_data)
#                     # recv_thread.daemon = True
#                     recv_thread.start()
#
#
# #--------------------------------------------------------------------------------------------------------------
#
#
#
#
# if __name__ == '__main__':
#     app = wx.App()
#     user = Log_in(work_sheet,work_book)
#     user.Show()
#     app.MainLoop()




client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect(('127.0.0.1',8887))
data = input(":")
while data != 'exit':
    client_socket.send(data.encode('utf-8'))
    data = input(':')
    if data == 'exit':
        client_socket.close()
