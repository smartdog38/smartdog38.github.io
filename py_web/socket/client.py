import threading #多线程
import wx #图表
from socket import socket,AF_INET,SOCK_STREAM #TCP通信需要引入
from threading import Thread


class chat_client(wx.Frame):
    def __init__(self,client_name):
        wx.Frame.__init__(self,None,id=1001,title=client_name+'的客户端界面',pos=wx.DefaultPosition,size=(400,450))#引入父类的初始化，并赋值
        pl = wx.Panel(self)#用wx的Panel函数设置面板
        box = wx.BoxSizer(wx.VERTICAL)#用wx的BoxSizer函数来初始化盒子，用VERTICAL来规定盒子方向为竖直方向
        fgzl = wx.FlexGridSizer(wx.HSCROLL)#用wx的FlexGridSizer函数来可变网格，HSCROLL来规定为横向
        #设置按钮，规定到面板里，面积大小（单位是像素），设置按钮名
        connect_btn = wx.Button(pl,size=(200,40),label='连接')
        dis_connect_btn = wx.Button(pl, size=(200, 40), label='断开')
        #将按钮添加到网格里，1为随便的参数，LEFT来规定按钮位置（其实没啥必要）
        fgzl.Add(connect_btn,1,wx.TOP | wx.LEFT)
        fgzl.Add(dis_connect_btn, 1, wx.TOP | wx.RIGHT)
        box.Add(fgzl,1,wx.ALIGN_CENTRE)#将网格加入到盒子里
        self.show_text = wx.TextCtrl(pl,size=(400,210),style=wx.TE_MULTILINE|wx.TE_READONLY)#用TextCtrl设置一个只读文本框，规定面板，大小，TE_MULTILINE为多行可读文本，TE_READONLY只读
        box.Add(self.show_text,1,wx.ALIGN_CENTRE)#加到盒子里，随机参数，ALIGN_CENTRE放在盒子中间
        self.chat_text = wx.TextCtrl(pl,size=(400,120),style=wx.TE_MULTILINE)#可写
        box.Add(self.chat_text,1,wx.ALIGN_CENTRE)#加到盒子里
        fgzl_2 = wx.FlexGridSizer(wx.HSCROLL)
        reset_btn = wx.Button(pl,size=(200,40),label='重置')
        send_btn = wx.Button(pl,size=(200,40),label='发送')
        fgzl_2.Add(reset_btn,1,wx.BOTTOM|wx.LEFT)#BOTTOM放底部
        fgzl_2.Add(send_btn,1,wx.BOTTOM|wx.RIGHT)
        box.Add(fgzl_2,1,wx.ALIGN_CENTRE)
        pl.SetSizer(box)#将盒子放进面板里

        #--------------------------------------------------
        self.Bind(wx.EVT_BUTTON,self.connect_server,connect_btn)#按钮绑定事件，函数不加括号
        self.Bind(wx.EVT_BUTTON, self.sent_to_server, send_btn)
        self.Bind(wx.EVT_BUTTON, self.dis_connect_server, dis_connect_btn)
        self.Bind(wx.EVT_BUTTON, self.reset_server, reset_btn)
        self.client_name = client_name #实例属性
        self.isconnent = False#表示连接状态
        self.client_socket = None#表示通道状态

    #重置操作
    def reset_server(self,event):#操作要给一个event参数！！！！！！！！
        self.chat_text.Clear()#

    #断连操作
    def dis_connect_server(self,event):
        self.client_socket.send('request to disconnect'.encode('utf-8'))#发送断连短信给服务器，让服务器也断开通信
        self.isconnent = False#把连接状态转回未连接状态
    #连接操作
    def connect_server(self,event):
        print("连接服务器成功")
        if self.isconnent == False:#当没连接时，进行下面操作
            server_host_port = ('127.0.0.1',7777)#给出服务器的IP地址与端口
            self.client_socket = socket(AF_INET,SOCK_STREAM)#建立套接字
            self.client_socket.connect(server_host_port)#尝试连接服务器
            self.client_socket.send(self.client_name.encode("utf-8"))#发送客户端名，进行身份识别
            client_thread = threading.Thread(target=self.recev_data_show)#创建客户端线程，规定目标函数
            client_thread.daemon = True#守护进程，只剩下守护线程时就会关闭该py文件
            self.isconnent = True#改变连接状态
            client_thread.start()#开始进程
    def sent_to_server(self,event):
        if self.isconnent:#判断是否连接
            input_data = self.chat_text.GetValue()#将聊天框内的内容赋值给变量
            if input_data != '':#如果不为空
                self.client_socket.send(input_data.encode('utf-8'))#就将变量信息发送出去
                self.chat_text.SetValue('')#清空聊天框

    #如果是连接状态，就不断接受信息，用AppendText表示在显示框
    def recev_data_show(self):
        while self.isconnent:
            data = self.client_socket.recv(1024).decode('utf-8')
            self.show_text.AppendText('-'*40+'\n'+data+'\n')



if __name__ == '__main__':
    app = wx.App()#app初始化，必要
    client = chat_client('mode')#创建实例，赋值给client_name
    client.Show()#显示，必要
    app.MainLoop()#重复刷新,如果没有新内容就保持不变，不会退出，如果有新内容就更新

