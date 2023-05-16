# 前后端一键化部署工具
- Nginx + uWSGI + Django

### 参数说明
```
Options:
  -f, --front-end TEXT  the dist directory of front-end  [required]
  -b, --back-end TEXT   the directory of back-end  [required]
  -n, --name TEXT       the name of django project  [required]
  -d, --directory TEXT  the directory to deploy  [default: ./deploy]
  -p, --port INTEGER    the port number  [default: 1080]
  -y, --force           force overwrite directory
  -?, -h, --help        Show this message and exit.
```

### 使用示例
```bash
deploy_django_nginx \
  -b /path/to/api  \                  # 后端根目录
  -f /path/to/app/dist/ \             # 前端dist目录
  -n proj \                           # Django项目名称
  -p 1080 \                           # 网络端口[可不写，会自动检查]
  -d /data2/work/novodb/beet \        # 生成目录
```
