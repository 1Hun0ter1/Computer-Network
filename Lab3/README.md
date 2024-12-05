# Lab3 Web Server

## 文件说明：
client -> get request ->  server (监听，返回一个文件)
```
Lab3/
├── server.py    (服务器监听)
├── client.py    (用户端发送)
├── index.html   (需要发送的文件)
├── config.ini   (安全配置文件)
├── server.log   (日志记录)
└── README.md    
```

## 终端命令：

首先在一个终端运行：

```
python server.py 
```

接着新开启一个终端运行：

```
python client.py 
```

如果需要测试：

```
python test_client.py
```



