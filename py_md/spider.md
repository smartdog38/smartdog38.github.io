# SPIDER

---
### 爬虫的工作
- **直接提取**  
想要的数据直接全部展示在页面源代码里，直接用特征提取。


- **间接提取**  
浏览器发送请求的时候，只返回部分信息乃至网页结构，当访问其内容时，再发送请求，带回所要的数据。


---
### 开发者工具
1. **Network(网络)**  

Headers(头):  

- General
>URl  当前网页的请求地址  
>Method  请求方式(get/post)  
>Code  状态码(200/404/500/303...)
- Request Header    
>User-Agent  用户用于访问的设备  

Preview(预览)  
展示响应的内容  

Paylaod(装载)  
会显示一些参数，里面的 Query String Parameters 会放进 url 里，而 From data 不会。

Response(响应)  
浏览器返回的数据  


2. **Source(源)**  
 有些js文件，包括页面源代码都再里面有


3. **Console(控制台)**  
可以调试代码


4. **Element(元素)**  
经过了修饰，可以作为参考，但不能依赖。


---
### requests 模块

- **发送请求**(*get请求*)  

`respon = requests.get(url)`  
返回状态码  
`respon.text`  
返回响应体的内容  
`repon.content`  
返回二进制数据  

但上面的请求容易给网页发现是爬虫，所以需要给其加上 `User-Agent` 即再Request Header里的。
将其放进字典里  

`header ={"User-Agent":"...."}`

然后加进 request 里   
`request(url,header)`  
当有参数时，将其存入字典，然后传进requests  
`requests.get(url=url,params=dict,headers=headers)`

- **发送请求**(*post请求*)  

`respon = requests.post(url=url,header=header,data=data)`  
也是状态码，加上 `.text`，得到响应的数据。
data是当中payload里包含的参数。如  
`data = { "key":"dad" }`

---
### 正则表达式（必要）
- `.` 能匹配除了换行符以外的所有内容，单个匹配，如果是 `..` 就两个两个匹配。换行符不匹配，但是不会断。

- `\w` 匹配数字，字母，下划线。

- `\s` 匹配空白字符

- `\d` 匹配数字

- `^` 开头

- `$` 结尾

- `*` 匹配前面的子表达式零次或多次

- `?` 匹配前面的子表达式零次或一次

- `{n}` n 是一个非负整数。匹配确定的 n 次。

- `{n,}` n 是一个非负整数。至少匹配n 次。

- `+` 匹配前面的子表达式一次或多次。

- `\` 用于转义其他特殊字符的转义符号。它具有最高的优先级。

- `()` 用于创建子表达式，具有高于其他运算符的优先级。 

- `[]` 用于匹配括号内的任意字符。

- `|` 用于在多个模式之间选择一个。

**重要表达式**
- `.*`  
贪婪匹配，匹配更多的结果


- `.*?`  
只匹配一次结果，不再多匹配。

---
### re 模块
PS: `r"..."` 可以忽略掉 `"\"` 的转义。

- `findall(r"...","re的东西")`

返回一个列表，如果没有就返回空列表。当用(.*?)时，findall会返回括号内的内容

- `finditer(r"...","re的东西")`

返回的是一个迭代器，循环取得 match 对象，要循环通过 `.group()` 得到结果。当用(.*?)时，finditer会返回括号内的内容加上检索的内容。

- `find(r"...","re的东西")`

返回的是第一个值。

- `search(re"...","re的东西")`

返回的也是match，也是要由 `.group()` 取得值，返回搜索到的第一个结果。


> 可以在开始匹配之前，先加载正则  
> 
> `obj = re.compile(re"...")`  
> `obj.finditer("re的东西")`  
> `obj.search("re的东西")`  
> `obj.findall("re的东西")`  
> 
> 不需要再加载

---
### CSS选择器类型
- 子代选择器  
在找到外层标签后，只找一层内部标签。

- 后代选择器  
在找到外层标签后，可以找多层内部标签。

- 类选择器  
找到指定类的标签。  
`.类名`

---
### bs4 模块

将页面源代码塞进 `BeautifulSoup(源代码,'html.parser')`

html.parser 是HTML解释器

先在源代码里找到大概的位置，在根据特征用

`.find("标签",attrs={"属性":"值"})`  

来找到标签，如果是

`find_all("标签",attrs={"属性":"值"})`

后面加 `[n]` 也可以找到标签

想要从标签里拿到属性，用

`标签.get("属性名")`















---
### ffmpeg
` subprocess.run([`  
     ``   "ffmpeg", ``   
    ``    "-f", "concat",  ``  
     ``   "-safe", "0",  ``  
  ``      "-i", ts_list_path,  ``  
    ``    "-c", "copy",  ``  
     ``   output_file_path  ``  
   `` ], check=True)  ``  

---
#### json 格式
json 格式类似于 python 的字典的字符串，即 ` '{"jjj":odwdj}' `，但是不能直接进行处理
需要调用 json 模块， `  import json `，然后通过 `json.loads( "json格式的东西" )`，就可以将其转换为字典格式。
，而想要将字典格式换为json格式，就用 `json.dums( "字典格式的东西" )`