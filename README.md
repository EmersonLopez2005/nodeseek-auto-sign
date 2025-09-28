```markdown
# 多站点Cookie签到脚本

支持NodeSeek和DeepFlood两个站点的多账户Cookie签到，解决Telegram通知频繁发送问题。

## 特点
- ✅ 纯Cookie登录，避免CF机器人检测
- ✅ 双站点支持（NodeSeek + DeepFlood）
- ✅ 多账户管理
- ✅ 通知优化（每天只发送一次汇总）

## 青龙面板使用

### 1. 拉取脚本
```bash
ql repo https://github.com/EmersonLopez2005/nodeseek-auto-sign.git
```

### 2. 配置环境变量
```bash
# NodeSeek Cookie（多个用&分隔）
NS_COOKIE=cookie1&cookie2&cookie3

# DeepFlood Cookie（多个用&分隔）
DF_COOKIE=cookie1&cookie2&cookie3

# Telegram通知配置
TG_BOT_TOKEN=你的机器人Token
TG_USER_ID=你的用户ID
```

### 3. 添加定时任务
```bash
30 8 * * * python3 /ql/scripts/EmersonLopez2005/multi_site_sign_cookie_only.py
```

## Cookie获取方法
1. 浏览器登录对应网站
2. F12 → Network → 找到请求 → Headers → Cookie
3. 复制完整Cookie值到环境变量

## 通知配置
脚本使用notify.py模块发送通知，支持多种通知方式。
```

### 3. .gitignore（可选）
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# 运行时文件
cookie/
*.log
*.txt

# 环境变量
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## 🔔 Telegram通知配置

### Telegram通知在notify.py文件中

你需要在青龙面板配置以下环境变量来启用Telegram通知：

```bash
# 必需的Telegram配置
TG_BOT_TOKEN=你的机器人Token        # 例：1407203283:AAG9rt-6RDaaX0HBLZQq0laNOh898iFYaRQ
TG_USER_ID=你的用户ID              # 例：1434078534

# 可选的Telegram配置
TG_THREAD_ID=                      # 超级群组话题ID（可选）
TG_API_HOST=                       # 代理API地址（可选）
TG_PROXY_HOST=                     # 代理主机（可选）
TG_PROXY_PORT=                     # 代理端口（可选）
TG_PROXY_AUTH=                     # 代理认证（可选）
```

### 如何获取Telegram配置

1. **创建机器人获取Token：**
   - 在Telegram中找到 @BotFather
   - 发送 `/newbot` 创建新机器人
   - 按提示设置机器人名称
   - 获得类似 `1407203283:AAG9rt-6RDaaX0HBLZQq0laNOh898iFYaRQ` 的Token

2. **获取用户ID：**
   - 在Telegram中找到 @userinfobot
   - 发送任意消息给它
   - 它会回复你的用户ID，例如：`1434078534`

3. **测试配置：**
   - 向你的机器人发送 `/start`
   - 确保机器人能收到消息

## 🚀 青龙面板完整配置流程

### 1. 拉取仓库
```bash
# 在青龙面板的订阅管理中添加
名称: 多站点签到
类型: public仓库
链接: https://github.com/EmersonLopez2005/nodeseek-auto-sign.git
定时: 0 0 * * *
白名单: multi_site_sign_cookie_only.py
```

### 2. 环境变量配置
在青龙面板环境变量中添加：

```bash
# 站点Cookie配置
NS_COOKIE=你的NodeSeek_Cookie1&你的NodeSeek_Cookie2
DF_COOKIE=你的DeepFlood_Cookie1&你的DeepFlood_Cookie2

# Telegram通知配置
TG_BOT_TOKEN=你的机器人Token
TG_USER_ID=你的用户ID

# 可选配置
NS_RANDOM=true
HITOKOTO=true
```

### 3. 定时任务
```bash
# 每天早上8:30执行
30 8 * * * python3 /ql/scripts/EmersonLopez2005/multi_site_sign_cookie_only.py
```

## 📝 总结

你只需要上传这4个文件到GitHub：
1. **multi_site_sign_cookie_only.py** - 主脚本
2. **notify.py** - 通知模块（已存在）
3. **requirements.txt** - 依赖包列表（需创建）
4. **README.md** - 项目说明（需创建）

然后在青龙面板配置Cookie和Telegram通知环境变量即可使用！
