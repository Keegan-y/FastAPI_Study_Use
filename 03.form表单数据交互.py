#encoding:utf-8
from starlette.requests import Request
from fastapi import FastAPI,Form###看完源码，Form很强大
from starlette.templating import Jinja2Templates

app=FastAPI()###类的实例化，创建一个FastAPI的实例
tmp=Jinja2Templates(directory='templates')

@app.get('/')###接收get请求
async def get_user(request:Request):###必须给request形参赋值
    ###print(tmp.TemplateResponse('form.html',{'request':request}))
    ###<starlette.templating._TemplateResponse object at 0x0000024E8DC76588>
    return tmp.TemplateResponse(name='form.html',context={'request':request})###必须给request形参赋值
    ###给get请求做出响应的

@app.post('/user/')###接收post请求
async def get_user(request:Request,
                   username:str=Form(...),
                   #直接去请求提里面获取username键对应的值并且自动的转化为字符串类型。
                   pwd:int=Form(...)
                   #直接去请求体里面获取pwd键对应的值并自动转化为整型。
                   ):
    print(username,type(username))
    print(pwd,type(pwd))
    return tmp.TemplateResponse('form.html',{
        'request':request,
        'username':username,
        'pwd':pwd
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8080)