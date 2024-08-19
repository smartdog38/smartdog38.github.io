import time
import wx
from socket import socket,AF_INET,SOCK_STREAM
import threading

class chat_server(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,id=1002,title='会议ing',pos=wx.DefaultPosition,size=(400,450))
        pl = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        fgzl = wx.FlexGridSizer(wx.HSCROLL)
        start_server_btn = wx.Button(pl,size=(133,40),label='启动服务')
        record_btn = wx.Button(pl,size=(133,40),label='保存聊天')
        stop_server_btn = wx.Button(pl,size=(133,40),label='停止服务')
        fgzl.Add(start_server_btn,1,wx.TOP)
        fgzl.Add(record_btn,1,wx.TOP)
        fgzl.Add(stop_server_btn,1,wx.TOP)
        box.Add(fgzl,1,wx.ALIGN_CENTRE)
        self.show_text = wx.TextCtrl(pl,size=(400,410),style=wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(self.show_text,1,wx.ALIGN_CENTRE)
        pl.SetSizer(box)
        # 界面绘制-------------------------------------------------------
        #服务器状态
        self.isON = False
        #设置服务器的IP地址与端口，''代表本机IP地址
        self.host_port = ('',7777)
        #建立套接字
        self.server_socket = socket(AF_INET,SOCK_STREAM)
        #套接字绑定IP与端口
        self.server_socket.bind(self.host_port)
        #监听通道（设置最大通信数量）
        self.server_socket.listen(5)
        #绑定按钮
        self.Bind(wx.EVT_BUTTON,self.start_server,start_server_btn)
        self.Bind(wx.EVT_BUTTON, self.save_record, record_btn)
        self.Bind(wx.EVT_BUTTON, self.stop_server, stop_server_btn)
        #字典存储会话线程
        self.session_thread_dict = {}
    #停止服务操作
    def stop_server(self,event):
        print("服务器停止服务")
        self.isON = False#改变服务器状态为关闭
    #保存记录操作
    def save_record(self,event):
        data = self.show_text.GetValue()#将显示框的记录赋值给变量
        with open('record.log','w',encoding='utf-8') as f:#写入文件
            f.write(data)
    #将信息写到显示框，并发送给客户端
    def show_info_return(self,data_source,data,datatime):#消息源，消息，发送时间
        send_data = f"{data_source}:{data}\n发送时间：{datatime}"
        self.show_text.AppendText('-'*40+'\n'+send_data+'\n')
        for client in self.session_thread_dict.values():#client是Session_Thread类的实例
            if client.isON:#相当于Session_Thread里的self.isON，表明该线程是打开状态
                client.client_socket.send(send_data.encode('utf-8'))#相当于client_socket.send(send_data.encode('utf-8'))



    def start_server(self,event):
        if self.isON == False:
            self.isON = True
            main_threading = threading.Thread(target=self.start_server_work)#没有括号，规定服务进程的函数
            main_threading.daemon = True
            main_threading.start()#开始主进程

    #主进程
    def start_server_work(self):
        while self.isON:
            session_socket,client_addr = self.server_socket.accept()#客户端发来的套接字请求，与客户段地址
            user_name = session_socket.recv(1024).decode("utf-8")#通过客户端发送的第一条消息给客户命名
            session_thread = Session_Thread(session_socket,user_name,self)#将套接字通道与用户名和服务器给Session_Thread的一个线程实例
            self.session_thread_dict[user_name] = session_thread
            session_thread.start()#执行子进程
            self.show_info_return('服务器通知',f'欢迎{user_name}进入会议',time.strftime('%Y-%m-%d  %H-%M-%S',time.localtime()))
        self.server_socket.close()
#因为服务器可能不只有一个通话，所以建立一个类来初始化通话实例
class Session_Thread(threading.Thread):
    def __init__(self,client_socket,user_name,server):#初始化，传入一个套接字，用户名，与服务器的self，所以这里的 server = 服务器里的 self，可以通过self.server.来调用chat里的方法与属性
        threading.Thread.__init__(self)#可以不给参数
        self.user_name = user_name#客户名
        self.server = server#服务器
        self.client_socket = client_socket#接受来自客户端的套接字通道
        self.isON = True#服务器对于该线程的通信保持打开

    def run(self) -> None:#线程启动时自动启动
        # print(f"客户端{self.user_name}已经进入会议！")
        while self.isON:#如果该线程的服务器是打开的状态
            data = self.client_socket.recv(1024).decode("utf-8")#连续收信息
            if data == 'request to disconnect':
                self.server.show_info_return('服务器通知',f'{self.user_name}离开了会议',time.strftime('%Y-%m-%d  %H-%M-%S',time.localtime()))
                self.isON = False#
        self.client_socket.close()#关闭该套接字连接


if __name__ == '__main__':
    app = wx.App()
    server = chat_server()
    server.Show()
    app.MainLoop()

