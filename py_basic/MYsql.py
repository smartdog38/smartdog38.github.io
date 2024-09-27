import wx


class AutoCompleteFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="自动补全示例")
        panel = wx.Panel(self)

        self.label = wx.StaticText(panel, label="输入内容：", pos=(10, 10))

        # 创建 ComboBox，允许用户输入及下拉补全
        self.combo_box = wx.ComboBox(panel, pos=(100, 10), style=wx.CB_DROPDOWN)
        self.combo_box.Bind(wx.EVT_COMBOBOX, self.on_combobox_select)

        # 设置一些示例选项
        self.options = ["苹果", "香蕉", "樱桃", "日期", "蓝莓", "草莓", "橙子"]
        self.combo_box.AppendItems(self.options)

        # 绑定文本输入事件
        self.combo_box.Bind(wx.EVT_TEXT, self.on_text_enter)

    def on_text_enter(self, event):
        input_value = self.combo_box.GetValue()
        if input_value:  # 如果输入不为空
            # 根据输入进行匹配并更新下拉框
            matching_options = [option for option in self.options if option.startswith(input_value)]
            self.combo_box.Clear()  # 清空当前选项
            self.combo_box.AppendItems(matching_options)  # 添加匹配的选项

            if matching_options:
                self.combo_box.SetValue(input_value)  # 保持用户输入的值
                self.combo_box.SetSelection(len(input_value))  # 将光标移动到文本末尾
            else:
                self.combo_box.SetValue(input_value)  # 无匹配则保持用户输入的值

    def on_combobox_select(self, event):
        selected_value = self.combo_box.GetValue()
        wx.MessageBox(f"您选择了: {selected_value}", "选择结果", wx.OK | wx.ICON_INFORMATION)


if __name__ == "__main__":
    app = wx.App(False)
    frame = AutoCompleteFrame()
    frame.Show()
    app.MainLoop()