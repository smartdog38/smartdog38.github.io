## 爬虫知识总结
### 我目前已经掌握的部分爬虫知识：
> 我们使用爬虫会遇到的情况
>> * 我们要爬的资源就在网页源代码里
> 
>> * 我们要爬的东西不在页面源代码里，需要去找到真正加载数据的那个请求，然后去提取数据

---
需要注意的是，网页源代码与开发者工具里的element不是一会事！！！element是页面源代码经过浏览器的加工后（实时体现）  
而我们写的爬虫程序拿到的是页面源代码！！！一定要以页面源代码为准！！！  
但是可以将element当做参考，结合一下效率会更高（element里有个查找的功能，可以快速定位所需要的东西的位置）  
---
下面是我们未来写爬虫最主要用到工具
> 开发者工具
> > element
> >> 页面实时代码
> 
> > network
> >> 网络的请求，后期抓包就是在这里
> 
> > resource
> >> 页面所有的数据包
> 
> > console
> >> 网页的控制台，可以输入要调试的页面代码
---
现在，我们可以通过network（上面提及的工具），来了解一些概念了
>
> > Headers
> >>头，含有cookies、user-agent、请求方式（get、post）、Status Code（请求状态）
> 
> >Response
> >>该数据包返回的源代码数据
> 
> >Preview
> >>返回数据包的预加载，也就是返回的数据在页面的样子
---
#### 申请的两种方式
>通过Headers里的请求方式来选择进行请求
> >get
> >
> > get请求的payload里是From Data是不需要怼到网页的url里
> >> `page = requests.get(url=url,headers=headers)`
> >
> > 返回的是状态码,
> >> `page = requests.get(url=url,headers=headers).text`
> >
> > 返回的才是数据,但是有时返回的是json数据，可以
> 
> >post
> >
> > post请求的payload里是Qurry String Parameters是需要怼到网页的url里，你可以在网页的url里发现里面的内容，是字典的形式
> >> `page = requests.post(url=url,headers=headers,data=data)`
> >
> > 其中的data
> >> `
> data = {"??":"??"}`
> >
> > 
> 
> 如果返回的数据是乱码，那么需要用 `.decode("utf-8")` 或其他来解码，如果，返回的是json形式，可以用以下两个方式
> > `import json`
> > 
> > `dic = json.loads(page.text)`
> >
> > 无论是json格式还是html格式都能用
> 
> 
> 或者
>
> > 
> > `dic = page.json()`
> >
> > 只能作用于json格式
> 
---

![](https://p1.ssl.qhimg.com/t01c3f58f10448fc470.jpg)
![](https://p9-pc-sign.douyinpic.com/tos-cn-i-0813c001/oUnVANBYQC0KtIDfTb9HAEVAz6oeogBoAiAA8l~noop.jpeg?biz_tag=pcweb_cover&from=327834062&s=PackSourceEnum_SEARCH&se=false&x-expires=1720231200&x-signature=11sSQCz41WnUaxGyY6xwcVk0J0w%3D)
![](https://p3-pc-sign.douyinpic.com/tos-cn-i-0813/og4He6yqyENAAAABRCYfqDLhImzANkAMUgtcaN~noop.jpeg?biz_tag=pcweb_cover&from=327834062&s=PackSourceEnum_SEARCH&se=false&x-expires=1720065600&x-signature=M0OUuDudPiC6jaZ6cT8dysyU2jE%3D)
![](https://altselection.com/wp-content/uploads/2024/04/Minnie-de-GI-DLE-758x481.jpg)
![](https://p26.toutiaoimg.com/origin/pgc-image/38a1ab86928847d1ba48821cf1d84973?/1.jpg)