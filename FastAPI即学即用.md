

# FastAPI框架

该框架的速度(天然支持异步)比一般的django和flask要快N多倍，号称可以比肩Go

使用该框架需要保证你的python解释器版本是3.6及以上

#### 安装虚拟环境

```python
C:\Users\YJG>mkvirtualenv FastAPI
    
(FastAPI) C:\Users\YJG>workon

Pass a name to activate one of the following virtualenvs:
==============================================================================
###省略其他虚拟环境
FastAPI

(FastAPI) C:\Users\YJG>    
```



#### 安装

```python
(FastAPI) F:\FastAPI>pip install fastapi
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple

(FastAPI) F:\FastAPI>pip install uvicorn###安装uvicorn来作为服务器
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple         
###安装完成！        

```

#### 基本使用

```python
from fastapi import FastAPI


app = FastAPI()


@app.get('/')  # 支持get请求
def read_root():
    return {"hello":'world'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8080)
```

运行程序之后，点击链接，会有以下结果：

http://ww1.sinaimg.cn/large/0067CtnRgy1gjzqakyajnj30cs02qweb.jpg

## 模版渲染

**安装**

```python
(FastAPI) F:\FastAPI>pip install jinja2
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
```

fastapi本身是没有模版渲染功能的，需要你借助于第三方的模版工具

该框架默认情况下也是借助于jinja2来做模版渲染

**基本使用**

```python
from starlette.requests import Request
from fastapi import FastAPI
from starlette.templating import Jinja2Templates


app = FastAPI()
# 挂在模版文件夹
tmp = Jinja2Templates(directory='templates')


@app.get('/')
async def get_tmp(request:Request):  # async加了就支持异步
    return tmp.TemplateResponse('index.html',
                                {'request':request,  # 一定要返回request
                                 'args':'hello world'  # 额外的参数可有可无
                                 }
                                )

@app.get('/{item_id}/')  # url后缀 
async def get_item(request:Request,item_id):
    return tmp.TemplateResponse('index.html',
                                {'request':request,
                                 'kw':item_id
                                 })


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8080)
```

## form表单数据交互

#### 提前安装这个模块：

```python
(FastAPI) F:\FastAPI>pip install python-multipart
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple

```



#### 基本数据

```python
from starlette.requests import Request
from fastapi import FastAPI,Form
from starlette.templating import Jinja2Templates


app = FastAPI()
tmp = Jinja2Templates(directory='templates')


@app.get('/')  # 接受get请求
async def get_user(request:Request):
    return tmp.TemplateResponse('form.html',{'request':request})


@app.post('/user/')  # 接受post请求
async def get_user(request:Request,
                   username:str=Form(...),  # 直接去请求体里面获取username键对应的值并自动转化成字符串类型
                   pwd:int=Form(...)  # 直接去请求体里面获取pwd键对应的值并自动转化成整型
                   ):
    print(username,type(username))
    print(pwd,type(pwd))
    return tmp.TemplateResponse('form.html',{
        'request':request,
        'username':username,
        'pwd':pwd
    })


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8080)
```

#### 文件交互

```python
from starlette.requests import Request
from fastapi import FastAPI, Form, File, UploadFile
from starlette.templating import Jinja2Templates
from typing import List

app = FastAPI()
tmp = Jinja2Templates(directory='templates')


@app.get('/')  # 接受get请求
async def get_file(request: Request):
    return tmp.TemplateResponse('file.html', {'request': request})


# 单个文件
@app.post('/file/')  # 接受post请求
async def get_user(request: Request,
                   file: bytes = File(...),
                   file_obj: UploadFile = File(...),
                   info: str = Form(...)
                   ):
    return tmp.TemplateResponse('index.html', {
        'request': request,
        'file_size': len(file),
        'file_name': file_obj.filename,
        'info':info,
        'file_content_type':file_obj.content_type
    })

# 多个文件
@app.post('/files/')
async def get_files(request:Request,
                    files_list:List[bytes] = File(...),  # [文件1的二进制数据,文件2的二进制数据]
                    files_obj_list:List[UploadFile]=File(...)  # [file_obj1,file_obj2,....]
                    ):
    return tmp.TemplateResponse('index.html',
                                {'request':request,
                                 'file_sizes':[len(file) for file in files_list],
                                 'file_names':[file_obj.filename for file_obj in files_obj_list]
                                 }
                                )

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8080)

```

```python
静态文件配置步骤及注意点：
（1）1个注意点需要pip 安装：
ModuleNotFoundError: No module named 'aiofiles'
    
(FastAPI) F:\FastAPI>pip install aiofiles
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
    
（2-1）步骤1：前端代码添加：
<!--静态文件配置-->
    <link rel="stylesheet" href="{{ url_for('static',path='/css/111.css') }}">
    <script src="{{ url_for('static',path='/js/111.js') }}"></script>
（2-2）步骤2：后端代码添加：
app=FastAPI()
# 挂载模版文件夹
tmp=Jinja2Templates(directory='templates')
# 挂载静态文件夹
app.mount('/static',StaticFiles(directory='static'),name='static')

```

#### 运行效果：

http://ww1.sinaimg.cn/large/0067CtnRgy1gjzqc5dl07j30bk0brwew.jpg