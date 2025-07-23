# nodeseek-auto-sign

```markdown
# NodeSeek 自动签到  
**iStoreOS 青龙面板 + CloudFreed（Turnstile）版**

> 账号密码 → 自建 CloudFreed 验证服务 → 自动拿 Cookie → 签到 → Telegram 推送  
> **无需公网 IP，家宽即可跑。**

---

## 🚀 一键部署（4 步）

### ① 安装青龙面板（iStoreOS）
```bash
docker run -d \
  --name qinglong \
  -p 5700:5700 \
  -v /root/qinglong:/ql/data \
  --restart unless-stopped \
  whyour/qinglong:latest
```
访问 `http://<iStoreOS_IP>:5700` 完成初始化。

---

### ② 下载脚本与依赖
进入容器：
```bash
docker exec -it qinglong bash
```
依次执行：
```bash
pip3 install requests

curl -o /ql/scripts/nodeseek_sign.py \
  https://raw.githubusercontent.com/EmersonLopez2005/nodeseek-auto-sign/main/sign.py
chmod +x /ql/scripts/nodeseek_sign.py
```

---

### ③ 部署 CloudFreed（Turnstile 验证服务）
仍在容器内：
```bash
mkdir -p /ql/cloudfreed
curl -o /ql/cloudfreed/server.js \
  https://raw.githubusercontent.com/EmersonLopez2005/nodeseek-auto-sign/main/cloudfreed/server.js

cd /ql/cloudfreed
npm init -y
npm install express
nohup node server.js > /dev/null 2>&1 &
```
验证服务已监听 `http://localhost:3000`。

---

### ④ 配置环境变量
**路径：青龙面板 → 环境变量 → 新建**

| 变量名 | 示例值 | 说明 |
|---|---|---|
| `USER1` | `alice` | 账号 |
| `PASS1` | `mySecretPwd` | 密码 |
| `USER2` / `PASS2` | … / … | 第二个账号（可选） |
| `CLIENTT_KEY` | `0x4AAAAAAAbCdEfGhIjKl` | **Cloudflare Turnstile Site Key** |
| `SOLVER_TYPE` | `turnstile` | **固定值** |
| `API_BASE_URL` | `http://localhost:3000` | **本地 CloudFreed 地址** |
| `TG_BOT_TOKEN` | `123456:ABC-DEF1234ghI` | Telegram Bot Token（可选） |
| `TG_USER_ID` | `987654321` | Telegram 用户 ID（可选） |

---

## ⏰ 定时任务
**路径：青龙面板 → 定时任务 → 新增**
- **名称**：`NodeSeek 自动签到`
- **命令**：`task nodeseek_sign.py`
- **定时规则**：`10 0 * * *`（每天 00:10）

---

## 🧪 立即测试
```bash
docker exec qinglong python3 /ql/scripts/nodeseek_sign.py
```

---

## 🔧 故障排查

| 现象 | 解决 |
|---|---|
| `未找到 token 或 sitekey` | 检查 NodeSeek 登录页结构变化 |
| `验证码破解失败` | 确认 CloudFreed 服务已启动 `curl http://localhost:3000` |
| `登录失败` | 检查账号密码、确认 Turnstile Site Key 正确 |

---

## 📄 脚本与验证服务
- 签到脚本：`https://raw.githubusercontent.com/EmersonLopez2005/nodeseek-auto-sign/main/sign.py`  
- CloudFreed 仓库：`https://github.com/EmersonLopez2005/cloudfreed`

---

> **无公网 IP，本地 CloudFreed 全自动完成 NodeSeek 签到。**

[![GitHub stars](https://img.shields.io/github/stars/EmersonLopez2005/nodeseek-auto-sign?style=flat-square)](https://github.com/EmersonLopez2005/nodeseek-auto-sign/stargazers)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)

