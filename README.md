# 前后端一键化部署工具
- Nginx + uWSGI + Django

### 参数说明
```
Options:
  -f, --front-end TEXT  the dist directory of front-end  [required]
  -b, --back-end TEXT   the build directory of back-end  [required]
  -n, --name TEXT       the name of project  [required]
  -d, --root TEXT       the root directory  [default: /data2/work/novodb]
  -p, --port INTEGER    the port number  [default: 1080]
  -y, --force           force overwrite directory
  -h, -?, --help        Show this message and exit.
```

### 使用示例
```bash
deploy_django_nginx \
    -b /data2/work/linmeng/proj/novodb/beet/api/ \        # 后端根目录
    -f /data2/work/linmeng/proj/novodb/beet/app/dist/ \   # 前端dist目录
    -n demo \                                             # 项目名称
    -p 1080 \                                             # 网络端口[可不写，会自动检查]
    -d /data2/work/novodb \                               # 生成根目录[可不写，默认都部署到这里]
```
