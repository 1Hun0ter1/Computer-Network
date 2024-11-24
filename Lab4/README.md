# Lab4 Web Server

## 文件说明：
client -> get request ->  proxy  ( 若cache 中无 request )->   server (监听，返回一个文件)
client -> get request ->  proxy  ( 若cache 中有 request ) 直接返回

```
Lab4/
├── server.py    (服务器监听)
├── client.py    (用户端发送)
├── proxy.py    (中间代理转发)
├── downloads (存储爬取的图片)
├── uploads (本地模拟server的数据库)
├── cache (proxy 管理的缓存库)
├── config.ini (配置文件库)
└── README.md    
```

## 终端命令：

首先在一个终端运行：

```
python server.py 
```

接着新开启一个终端运行：

```
python proxy.py 
```

最后新开启一个终端运行：

```
python client.py 
```



## TODO

```
1.Release our code in the future. 

```

