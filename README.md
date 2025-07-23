
# NodeSeek 自动签到（FlareSolverr 版）

> **账号密码 → FlareSolverr 绕过 Cloudflare → 本地 CloudFreed 破解 Turnstile → 自动签到 → TG 推送**  
> **无需公网 IP，家宽即可跑。**

---

## 🚀 一键部署（4 步）

### ① 安装青龙面板
```bash
docker run -d \
  --name qinglong \
  -p 5700:5700 \
  -v /root/qinglong:/ql/data \
  --restart unless-stopped \
  whyour/qinglong:latest
```
浏览器访问 `http://<IP>:5700` 完成初始化。

---

### ② 下载脚本与依赖
进入容器：
```bash
docker exec -it qinglong bash
pip3 install requests
curl -o /ql/data/scripts/sign.py \
  https://raw.githubusercontent.com/EmersonLopez2005/nodeseek-auto-sign/main/sign_flare.py
chmod +x /ql/data/scripts/sign.py
```

---

### ③ 部署 FlareSolverr & CloudFreed
**FlareSolverr**（用于绕过 Cloudflare 5 秒盾）：
```bash
# 宿主机执行
docker run -d \
  --name flaresolverr \
  --network host \
  -e LOG_LEVEL=info \
  --restart unless-stopped \
  ghcr.io/flaresolverr/flaresolverr:latest
```

**CloudFreed**（本地 Turnstile 验证码服务）：
```bash
# 仍在容器内
mkdir -p /ql/cloudfreed
curl -o /ql/cloudfreed/server.js \
  https://raw.githubusercontent.com/EmersonLopez2005/nodeseek-auto-sign/main/cloudfreed/server.js
cd /ql/cloudfreed
npm init -y
npm install express
nohup node server.js > /dev/null 2>&1 &
```
验证：
```bash
curl http://localhost:3000   # CloudFreed
curl http://localhost:8191/health  # FlareSolverr
```

---

### ④ 配置环境变量
**路径：青龙面板 → 环境变量 → 新增**

| 变量名         | 示例值                           | 说明 |
|----------------|----------------------------------|------|
| `USER1`        | `alice@mail.com`                | 账号 |
| `PASS1`        | `mySecretPwd`                   | 密码 |
| `CLIENTT_KEY`  | `0x4AAAAAAAbCdEfGhIjKl`         | Turnstile Site Key |
| `SOLVER_TYPE`  | `turnstile`                     | 固定值 |
| `API_BASE_URL` | `http://localhost:3000`         | CloudFreed 地址 |
| `TG_BOT_TOKEN` | `123456:ABC-DEF1234ghI`         | TG Bot Token（可选） |
| `TG_USER_ID`   | `987654321`                     | TG 用户 ID（可选） |

---

## ⏰ 定时任务
**路径：青龙面板 → 定时任务 → 新增**
- **名称**：NodeSeek 自动签到（FlareSolverr 版）
- **命令**：`task sign.py`
- **定时规则**：`10 0 * * *`（每天 00:10）

---

## 🧪 立即测试
```bash
docker exec qinglong python3 /ql/data/scripts/sign.py
```

---

## 🔧 故障排查
| 现象 | 解决 |
|---|---|
| `Connection refused: 8191` | FlareSolverr 未启动或未映射 8191 |
| `未找到 token 或 sitekey` | NodeSeek 登录页结构变化，更新正则 |
| `验证码破解失败` | 检查 CloudFreed 服务 `curl http://localhost:3000` |
| `登录失败` | 检查账号密码、Turnstile Site Key |

---

## 📄 相关文件
- 签到脚本：`https://raw.githubusercontent.com/EmersonLopez2005/nodeseek-auto-sign/main/sign_flare.py`
- CloudFreed 服务：`https://raw.githubusercontent.com/EmersonLopez2005/nodeseek-auto-sign/main/cloudfreed/server.js`
- FlareSolverr：`https://github.com/FlareSolverr/FlareSolverr`

---

> **无公网 IP，本地 FlareSolverr + CloudFreed 全自动完成 NodeSeek 签到。**
```
