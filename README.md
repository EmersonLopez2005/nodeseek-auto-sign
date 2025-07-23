# nodeseek-auto-sign
nodeseek-auto-sign
部署步骤（以青龙面板为例）
1. 基础环境准备
bash
# 进入青龙容器
docker exec -it qinglong bash

# 安装 Python 依赖
pip3 install requests
2. 添加脚本文件
在青龙面板创建新脚本：

名称：nodeseek_sign.py

类型：Python

内容：粘贴完整代码

3. 配置环境变量
在青龙面板 → 环境变量 添加：

变量名	示例值	必填	说明
USER1	your@email.com	✔️	主账号邮箱
PASS1	your_password	✔️	主账号密码
CLIENTT_KEY	0x4AAAAAA...	❌	Turnstile Site Key
SOLVER_TYPE	turnstile	❌	固定值
API_BASE_URL	http://localhost:3000	❌	自建验证服务地址
TG_BOT_TOKEN	123456:ABC-DEF	❌	Telegram 机器人 Token
TG_USER_ID	987654321	❌	Telegram 用户 ID
📌 关键细节：

多账号支持：添加 USER2/PASS2, USER3/PASS3 等

验证码配置：

如果 Nodeseek 有验证码：必须配置 CLIENTT_KEY + SOLVER_TYPE=turnstile

无验证码：留空即可

Telegram 通知：按需配置

4. 验证码服务部署（可选）
如果需要破解 Turnstile 验证码，二选一：

方案 A：使用 CloudFreed（默认）

bash
# 在青龙容器内运行验证服务
docker exec -it qinglong bash
git clone https://github.com/EmersonLopez2005/cloudfreed.git
cd cloudfreed
npm install
node server.js  # 保持后台运行
