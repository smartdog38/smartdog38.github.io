import wx
from socket import socket,AF_INET,SOCK_STREAM
import time
from threading import Thread

command_dict = {
    'root': {'查询信息': {'用户信息': {
        'Wang': {'密码': '1234', '用户权限': 'common', '生日': '2004-08-17', '性别': '男', '居住地': '南京',
                 '注册时间': '2008-07-11'},
        'Lily': {'密码': '54321', '用户权限': 'common', '生日': '2004-06-27', '性别': '女', '居住地': '上海',
                 '注册时间': '2006-08-11'}}
        , '用户状态': {'Wang': 'down', 'Lily': 'down'}},
             '更改权限': {'Wang': 'common', 'Lily': 'common'},
             '关闭系统': 'lock'},
    'Wang': {
        '查询信息': {'密码': '1234', '生日': '2004-08-17', '性别': '男', '居住地': '南京',
                     '注册时间': '2008-07-11'},
        '获取当月财务报表': 'sxsxssxx'},
    'Lily': {
        '查询信息': {'密码': '54321', '生日': '1994-06-27', '性别': '女', '居住地': '上海',
                     '注册时间': '2008-07-11'},
        '获取当月财务报表': 'sxsxssxx'}
}

class server_answer(wx.Frame):
    def __init__(self):
        self.isON = False
        self.host_port = ('',8887)
        self.active_connections = []

#绘制服务器窗口（done）-----------------------------------------------------------------------------------------------------
        wx.Frame.__init__(self,None,id=1222,pos=wx.DefaultPosition,title='英雄库',size=(550,550))
        pl = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        ff = wx.FlexGridSizer(wx.HSCROLL)
        server_btn = wx.Button(pl,size=(200,40),label='开始服务')
        stop_server_btn = wx.Button(pl,size=(200,40),label='停止服务')
        ff.Add(server_btn,1,wx.TOP|wx.ALL,10)
        ff.Add(stop_server_btn,1,wx.TOP|wx.ALL,10)
        self.read_text = wx.TextCtrl(pl,size=(500,450),style=wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(ff,1,wx.ALIGN_CENTRE|wx.ALL,10)
        box.Add(self.read_text,1,wx.ALIGN_CENTRE|wx.ALL,10)
        pl.SetSizer(box)
#绑定事件-----------------------------------------------------------------------------------------------------------------
        self.Bind(wx.EVT_BUTTON,self.start_server,server_btn)
        self.Bind(wx.EVT_BUTTON,self.stop_server,stop_server_btn)
#定义事件-----------------------------------------------------------------------------------------------------------------

#开始服务事件
    def start_server(self,event):
        if self.isON == False:
            self.isON = True
            self.socket_server = socket(AF_INET, SOCK_STREAM)
            self.socket_server.bind(self.host_port)
            self.socket_server.listen(5)
            self.read_text.AppendText("服务开启\n" + time.strftime('%Y-%m-%d %H:%M-%S', time.localtime()) + '\n')
            main_thread = Thread(target=self.start_work)
            main_thread.daemon = True
            main_thread.start()

#主进程事件
    def start_work(self):
        while self.isON:
            session_socket,client_addr = self.socket_server.accept()#接收一个套接字
            self.active_connections.append(session_socket)
            username = session_socket.recv(1024).decode('utf-8')#将第一次的接受信息当作名字
            if username not in command_dict.keys():
                sign_date = time.strftime('%Y-%m-%d', time.localtime())
                session_socket.send("\n请输入你的密码，生日，性别，居住地（以英文的逗号隔开，日期以‘1000-12-03’为标准）\n".encode('utf-8'))
                data = session_socket.recv(1024).decode('utf-8')
                data = data.split(',')
                passwd = data[0]
                date = data[1]
                sex = data[2]
                address = data[3]
                self.user_add(username,passwd,date,sex,address,sign_date)
            self.read_text.AppendText(f"\n{username}进入系统\n" + time.strftime('%Y-%m-%d %H:%M-%S', time.localtime()) + '\n')
            session_thread = session_Thread(session_socket,username,self)#创造一个会话进程实例，将套接字与名字和服务器一起传进实例
            session_thread.start()




    def user_add(self,username,passwd,date,sex,address,sign_date):
        command_dict[username] ={'查询信息': {'密码': f'{passwd}', '用户权限': 'common', '生日': f'{date}', '性别': f'{sex}', '居住地': f'{address}','注册时间': f'{sign_date}'},
                                '获取当月财务报表': 'sxsxssxx'}
        command_dict['root']['查询信息']['用户信息'][username]= {'密码': f'{passwd}', '用户权限': 'common', '生日': f'{date}', '性别': f'{sex}', '居住地': f'{address}','注册时间': f'{sign_date}'}
        command_dict['root']['查询信息']['用户状态'][username] = 'down'
        command_dict['root']['更改权限'][username] = 'common'


    def stop_server(self,event):
        if self.isON:
            self.isON = False
            # 断开所有活动连接
            for conn in self.active_connections:
                conn.close()
            self.active_connections.clear()  # 清空活动连接列表
            data = self.read_text.GetValue()
            with open(f"D:\\PyCharm Community Edition 2023.3\\py_study\\record_{time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())}.log", "w", encoding="utf-8") as f:
                f.write(data)
            self.read_text.Clear()
            self.socket_server.close()
            self.read_text.AppendText("\n\n服务已停止\n" + time.strftime('%Y-%m-%d %H:%M-%S', time.localtime()) + '\n\n')


class session_Thread(Thread):
    def __init__(self,client_socket,username,server):
        super().__init__()
        self.username = username#用self.username
        self.client_socket = client_socket
        self.server = server#后面调用直接server，引进类
        self.isON = True
    def run(self) -> None:
        while self.isON:
            self.check(self.username)
            data = self.client_socket.recv(1024).decode('utf-8')
            if not data :
                self.isON = False
                self.server.read_text.AppendText(f'\n{time.strftime("%Y-%m-%d %H:%M-%S", time.localtime())}\n{self.username}退出登录\n')
#用户操作语句--------------------------------------------------------------------------------------------------------------
#查询语句-----------------------------------------------------------------------------------------------------------------
    def check(self, username):
        if isinstance(command_dict[username],dict):
            options = '\n'.join(command_dict[username].keys())
            self.client_socket.send(f'{options}\n'.encode('utf-8'))
            order_0 = self.client_socket.recv(1024).decode('utf-8')
            while order_0 not in command_dict[username]:
                if not order_0:
                    self.server.read_text.AppendText(f'\n{time.strftime("%Y-%m-%d %H:%M-%S", time.localtime())}\n{self.username}退出登录\n')
                    break
                if order_0 =='exit':
                    self.client_socket.send("\n退出登录\n".encode('utf-8'))
                    order_0 = self.client_socket.recv(1024).decode('utf-8')
                else:
                    print(f"{order_0}")
                    self.client_socket.send("\n无效指令\n".encode('utf-8'))
                    order_0 = self.client_socket.recv(1024).decode('utf-8')
            if order_0:
                server.read_text.AppendText(f"\n用户 {username} 执行了 {order_0} 指令\n{time.strftime("%Y-%m-%d %H:%M-%S", time.localtime())}\n")
                self.order_o_act(username,order_0)
        else:
            self.client_socket.send(f"\n{command_dict[username]}\n".encode('utf-8'))
            self.client_socket.send("\n(输入任意值返回初始界面)\n".encode('utf-8'))



    def order_o_act(self,username,order_0):
        if isinstance(command_dict[username][order_0],dict):
            options = '\n'.join(command_dict[username][order_0].keys())
            self.client_socket.send(f"\n{options}\n".encode('utf-8'))
            order_1 = self.client_socket.recv(1024).decode('utf-8')
            while order_1 not in command_dict[username][order_0]:
                if not order_1:
                    self.server.read_text.AppendText(f'\n{time.strftime("%Y-%m-%d %H:%M-%S", time.localtime())}\n{self.username}退出登录\n')
                    break
                if order_1 == 'exit':
                    self.client_socket.send("\n退出登录\n".encode('utf-8'))
                    order_1 = self.client_socket.recv(1024).decode('utf-8')
                else:
                    self.client_socket.send("\n无效指令\n".encode('utf-8'))
                    order_1 = self.client_socket.recv(1024).decode('utf-8')
            if order_1:
                server.read_text.AppendText(f"\n用户 {username} 执行了 {order_1} 指令\n{time.strftime("%Y-%m-%d %H:%M-%S", time.localtime())}\n")
                self.order_1_act(username,order_0,order_1)
        else:
            self.client_socket.send(f"\n{command_dict[username][order_0]}\n".encode('utf-8'))
            self.client_socket.send("\n(输入任意值返回初始界面)\n".encode('utf-8'))

    def order_1_act(self,username,order_0,order_1):
        if isinstance(command_dict[username][order_0][order_1], dict):
            options = '\n'.join(command_dict[username][order_0][order_1].keys())
            self.client_socket.send(f"\n{options}\n".encode('utf-8'))
            order_2 = self.client_socket.recv(1024).decode('utf-8')
            while order_2 not in command_dict[username][order_0][order_1]:
                if not order_2:
                    self.server.read_text.AppendText(f'\n{time.strftime("%Y-%m-%d %H:%M-%S", time.localtime())}\n{self.username}退出登录\n')
                    break
                elif order_2 == 'exit':
                    self.client_socket.send("\n退出登录\n".encode('utf-8'))
                    order_2 = self.client_socket.recv(1024).decode('utf-8')
                else:
                    self.client_socket.send("\n无效指令\n".encode('utf-8'))
                    order_2 = self.client_socket.recv(1024).decode('utf-8')
            if order_2:
                server.read_text.AppendText(f"\n用户 {username} 执行了 {order_2} 指令\n{time.strftime("%Y-%m-%d %H:%M-%S", time.localtime())}\n")
                self.order_2_act(username, order_0, order_1,order_2)
        else:
            self.client_socket.send(f"\n{command_dict[username][order_0][order_1]}\n".encode('utf-8'))
            self.client_socket.send("\n(输入任意值返回初始界面)\n".encode('utf-8'))
    def order_2_act(self,username,order_0,order_1,order_2):
        if isinstance(command_dict[username][order_0][order_1][order_2], dict):
            options = '\n'.join(command_dict[username][order_0][order_1][order_2].keys())
            self.client_socket.send(f"\n{options}\n".encode('utf-8'))
            order_3 = self.client_socket.recv(1024).decode('utf-8')
            while order_3 not in command_dict[username][order_0][order_1][order_2]:
                if not order_3:
                    self.server.read_text.AppendText(f'\n{time.strftime("%Y-%m-%d %H:%M-%S", time.localtime())}\n{self.username}退出登录\n')
                    break
                elif order_3 == 'exit':
                    self.client_socket.send("\n退出登录\n".encode('utf-8'))
                    order_3 = self.client_socket.recv(1024).decode('utf-8')
                else:
                    self.client_socket.send("\n无效指令\n".encode('utf-8'))
                    order_3 = self.client_socket.recv(1024).decode('utf-8')
            if order_3:
                server.read_text.AppendText(f"\n用户 {username} 执行了 {order_3} 指令\n{time.strftime("%Y-%m-%d %H:%M-%S", time.localtime())}\n")
                self.order_3_act(username, order_0, order_1,order_2,order_3)
        else:
            self.client_socket.send(f"\n{command_dict[username][order_0][order_1][order_2]}\n".encode('utf-8'))
            self.client_socket.send("\n(输入任意值返回初始界面)\n".encode('utf-8'))
    def order_3_act(self,username,order_0,order_1,order_2,order_3):
        self.client_socket.send(f"\n{command_dict[username][order_0][order_1][order_2][order_3]}\n".encode('utf-8'))
        self.client_socket.send("\n(输入任意值返回初始界面)\n".encode('utf-8'))
#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.App()
    server = server_answer()
    server.Show()
    app.MainLoop()