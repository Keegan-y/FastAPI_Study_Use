#encoding:utf-8
from starlette.requests import Request
from fastapi import FastAPI,Form,File,UploadFile
from starlette.templating import Jinja2Templates
from typing import List

app=FastAPI()
tmp=Jinja2Templates(directory='templates')

@app.get('/')#接收get请求
async def get_file(request:Request):
    return tmp.TemplateResponse('file.html',{'request':request})

#处理单个文件
@app.post('/file/')#接收post请求
async def get_user(request:Request,
                   file:bytes=File(...),
                   file_obj:UploadFile=File(...),
                   info:str=Form(...),
                   ):
    return tmp.TemplateResponse('index.html',{
        'request':request,
        'file_size':len(file),
        'file_name':file_obj.filename,
        'info':info,
        'file_content_type':file_obj.content_type
    })
#处理多个文件
@app.post('/files/')
async def get_files(request:Request,
                    files_list:List[bytes]=File(...),###[文件1的二进制数据,文件2的二进制数据]
                    files_obj_list:List[UploadFile]=File(...)###[file_obj1,file_obj2,...]
                    ):
    return tmp.TemplateResponse('index.html',
                                {'request':request,
                                 'file_sizes':[len(file) for file in files_list],
                                 'file_names':[file_obj.filename for file_obj in files_obj_list]
                                 })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8080)###可看源码传参