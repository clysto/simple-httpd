# simple httpd

![CI](https://github.com/clysto/simple-httpd/workflows/CI/badge.svg)

## Quick Start

```bash
python3 main.py ./test/config.cfg
```

使用config.cfg配置文件启动http服务器，在浏览器中打开[http://localhost:3000](http://localhost:3000)即可看到页面默认页面。

## Description

这个项目是用来学习 http 相关内容，使用 Python3 编写了一个简易的 http 服务器。不依赖其他的库，仅使用原生 Python3 编程。

## Todo

- [x] 支持 index 列表
- [x] 支持多线程
- [x] 区分 http method
- [x] 支持 CGI 脚本程序
- [x] CGI中文乱码问题
- [ ] CGI返回状态码支持
