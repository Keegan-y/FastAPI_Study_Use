#encoding:utf-8
from fastapi import FastAPI

app = FastAPI()

@app.get('/')#支持get请求
def read_root():
    return {"hello":"world"}###get请求---响应的内容

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8080)