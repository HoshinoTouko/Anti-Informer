# Anti-Informer
A python application for secure communication. 

## About project

这是一个密码学的结课设计，目标是基于本学期的学习内容，构建一个安全的通信工具。

## About document

- 服务器API相关 [Link](ServerAPI.md)
- 密钥协议相关 [Link](KeyProtocol.md)

## Install

```
pip install -r requirements.txt
python manage.py migrate
```

## Run server
```
python manage.py runserver 0.0.0.0:8000
```

## Run client
```
python client.py
```
If you want to reset local data, just totally delete **.data/user/**

## Development reference

PyCryptodome: http://pycryptodome.readthedocs.io/en/latest/index.html
