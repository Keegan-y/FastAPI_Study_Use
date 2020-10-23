#encoding:utf-8
from starlette.requests import Request
from fastapi import FastAPI
from starlette.templating import Jinja2Templates

app = FastAPI()
###挂载模版文件夹
tem = Jinja2Templates(directory='templates')

@app.get('/')
async def get_tem(request:Request):###加了async就支持异步+给request赋值
    return tem.TemplateResponse('index.html',
                                {'request':request,#必须返回request
                                 'args':'hello world'
                                })

@app.get('/{item_id}/')###url后缀
async def get_item(request:Request,item_id):
    return tem.TemplateResponse('index.html',
                                {'request':request,
                                 'kw':item_id
                                })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8080)