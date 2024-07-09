# texstudio 论文写作

## title  
> `\title{}`   {里面放论文名}  
> 
> 通讯作者 ： 论文的组织者，在论文上会附上 电话 与 邮箱地址    
>   
> 电话
> 
>> `\author[rvt]{guangquan Hou\corref{cor1}}`  
>  `\cortext[cor1]{Corresponding author.`  
`Tel.: +86 0631 5678533; fax: +86 0631 5687660.}`
> 
> 邮箱
> 
> >`\ead{wenxuetg@hitwh.edu.cn,wenxue810823@163.com}`
> 
> 作者前的[ ]里放的是 单位（可以用`\adress[uuu]{单位名称}` 来直接通用）  在作者的前面直接加上[uuu]即可  
> 
> >`\author[rvt]{Gang Wang}`


## abstract 
> >`\begin{abstract}` 
> 
> 是摘要的开始端，在下面可以直接写摘要。
> 
> >`\end{abstract}` 
> 
> 是摘要的结尾。

## keyword
> >`\begin{keyword}`  
> 
> 是关键词的开始端 
> 
> 中间的关键词用;隔开
> 
> >`\end{keyword}`
> 
> 是关键词的结束


以上是整个frontmatter的内容。

## 正文部分(section)
> 是论文的介绍部分  
> 
> >`\section{Introduction}`
> 
> 
> 文本加粗
> 
> >`textbf{}`
>
> 
> 定理、证明  
> 
> 定理：
>> `\begin{thm}`  
> `content`  
> `\end{thm}`
> 
> 证明：
> >`\begin{proof}`  
> `content`  
> `\end{proof}`
> 
> 
> 引进文献  
> 
>  >` \citep{Steven,Boccaletti,Jonathan,Jiang2008,Jlu}`  
>   
> 会根据下面的文献顺序，改变文献对应的数字  
> 文献形式，下文会提及


## 区块
> 前面是点的区块
>>`\begin{itemize}`  
> `\item content`  
> `\item content`  
> `.....`  
> `\end{itemize}` 
> 
> 前面数字排序的区块
>> `\begin{enumerate}`  
> `\item content`  
> `\item content`  
> `.....`  
> `\end{enumerate}`
> 
> 其中的符号是自己想要的排序符 
>> `\begin{description}`  
> `\item[符号] content`  
> `\item[符号] content`  
> `.....`  
> `\end{description}`

