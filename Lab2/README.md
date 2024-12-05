# 示例

**单线程启动：**

```
python traceroute.py --destination www.youku.com --max-hops 30 --timeout 5 --retries 3 --protocol ICMP --save-format json 
```

**多线程启动：**

```
python traceroute.py --destination www.youku.com --max-hops 30 --timeout 5 --retries 3 --protocol ICMP --save-format json --async-mode
```

**Linux only：**

```
python traceroute.py --destination www.youku.com --max-hops 30 --timeout 3 --retries 3 --protocol UDP 
```



