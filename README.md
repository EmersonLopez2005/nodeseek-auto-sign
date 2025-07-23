# nodeseek-auto-sign
nodeseek-auto-sign

## 📦 安装与部署

### 1. 青龙面板配置

#### 添加脚本文件
1. 在青龙面板创建新脚本
2. 名称：`nodeseek_sign.py`
3. 类型：`Python`
4. 粘贴 [完整代码](https://github.com/EmersonLopez2005/nodeseek-auto-sign/blob/main/sign.py)

#### 配置环境变量
在青龙面板 → 环境变量 中添加：

| 变量名          | 示例值                  | 必填 | 说明                                                                 |
|-----------------|-------------------------|------|----------------------------------------------------------------------|
| `USER1`         | your@email.com          | ✔️   | 主账号邮箱                                                           |
| `PASS1`         | your_password           | ✔️   | 主账号密码                                                           |
| `USER2`         | another@email.com       | ❌   | 第二个账号邮箱（多账号支持）                                         |
| `PASS2`         | another_password        | ❌   | 第二个账号密码                                                       |
| `CLIENTT_KEY`   | 0x4AAAAAAAbCdEfGhIjKl   | ❌   | Turnstile Site Key ([获取方法](#cloudflare-turnstile-配置指南))      |
| `SOLVER_TYPE`   | turnstile               | ❌   | 验证码解决类型（固定值 `turnstile`）                                 |
| `API_BASE_URL`  | http://localhost:3000   | ❌   | 自建验证服务地址（默认使用项目自带服务）                             |
| `TG_BOT_TOKEN`  | 123456:ABC-DEF1234ghI   | ❌   | Telegram 机器人 Token ([创建教程](https://core.telegram.org/bots)) |
| `TG_USER_ID`    | 987654321               | ❌   | Telegram 用户 ID ([获取方法](https://t.me/userinfobot))            |

### 2. 验证服务部署（可选）
当 Nodeseek 启用验证码时需要：

```bash
# 进入青龙容器
docker exec -it qinglong bash

# 克隆验证服务
git clone https://github.com/EmersonLopez2005/cloudfreed.git

# 安装依赖
cd cloudfreed
npm install

# 启动服务（后台运行）
nohup node server.js > /dev/null 2>&1 &
```

#### 验证服务状态
```bash
# 检查进程
docker exec qinglong ps aux | grep node

# 测试服务响应
docker exec qinglong curl http://localhost:3000
```

### 3. 设置定时任务
在青龙面板 → 定时任务：
- 名称：`NodeSeek 自动签到`
- 命令：`task nodeseek_sign.py`
- 定时规则：`10 0 * * *` (每天 00:10 执行)

## ⚙️ Cloudflare Turnstile 配置指南
1. 访问 [Cloudflare Turnstile](https://dash.cloudflare.com/?to=/:account/turnstile)
2. 点击 "Add Site"
3. 配置站点：
   - Site name: `NodeSeek-AutoSign`
   - Domain: `www.nodeseek.com`
   - Widget Mode: Managed
4. 复制生成的 **Site Key** → 填入 `CLIENTT_KEY`

## 🔧 故障排查
### 常见错误解决方案
| 错误信息 | 解决方案 |
|----------|----------|
| `未找到 token 或 sitekey` | 1. 检查登录页结构是否变化<br>2. 更新正则表达式 |
| `验证码破解失败` | 1. 确认验证服务已启动<br>2. 检查端口是否冲突 |
| `登录失败，检查账号密码/验证码` | 1. 确认密码正确<br>2. 临时关闭验证码测试 |

### 手动测试命令
```bash
docker exec qinglong python3 /ql/scripts/nodeseek_sign.py
```

## ❤️ 贡献指南
欢迎提交 PR 改进项目：
1. Fork 本仓库
2. 创建新分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -m 'Add some feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 创建 Pull Request

[![GitHub stars](https://img.shields.io/github/stars/EmersonLopez2005/nodeseek-auto-sign?style=flat-square)](https://github.com/EmersonLopez2005/nodeseek-auto-sign/stargazers)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)

