# NodeSeek & DeepFlood 自动签到脚本

[![GitHub stars](https://img.shields.io/github/stars/EmersonLopez2005/nodeseek-auto-sign?style=flat-square)](https://github.com/EmersonLopez2005/nodeseek-auto-sign/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/EmersonLopez2005/nodeseek-auto-sign?style=flat-square)](https://github.com/EmersonLopez2005/nodeseek-auto-sign/network)
[![GitHub issues](https://img.shields.io/github/issues/EmersonLopez2005/nodeseek-auto-sign?style=flat-square)](https://github.com/EmersonLopez2005/nodeseek-auto-sign/issues)
[![GitHub license](https://img.shields.io/github/license/EmersonLopez2005/nodeseek-auto-sign?style=flat-square)](https://github.com/EmersonLopez2005/nodeseek-auto-sign/blob/main/LICENSE)

> 🚀 支持 NodeSeek 和 DeepFlood 两个论坛的多账户自动签到脚本，专为青龙面板优化

## ✨ 特性

- 🎯 **双站点支持** - 同时支持 NodeSeek 和 DeepFlood 论坛
- 🔐 **纯Cookie登录** - 避开Cloudflare机器人检测，稳定可靠
- 👥 **多账户管理** - 每个站点支持无限个账户
- 📱 **智能通知** - 每天只发送一次汇总通知，告别通知轰炸
- 🏷️ **自定义用户名** - 支持为每个账户设置个性化显示名称
- 📊 **签到统计** - 自动统计近30天签到收益
- 🐳 **多环境支持** - 青龙面板、Docker、GitHub Actions
- 🔄 **自动重试** - 网络异常自动重试机制

## 📦 快速开始

### 1. 青龙面板部署（推荐）

#### 拉取仓库
```bash
ql repo https://github.com/EmersonLopez2005/nodeseek-auto-sign.git
```

#### 配置环境变量
在青龙面板 `环境变量` 中添加：

```bash
# 必需配置
NS_COOKIE=你的NodeSeek_Cookie1&你的NodeSeek_Cookie2
DF_COOKIE=你的DeepFlood_Cookie1&你的DeepFlood_Cookie2
TG_BOT_TOKEN=你的Telegram机器人Token
TG_USER_ID=你的Telegram用户ID

# 可选配置（自定义用户名显示）
NS_USERNAMES=张三&李四&王五
DF_USERNAMES=用户A&用户B&用户C
```

#### 添加定时任务
```bash
30 8 * * * python3 /ql/scripts/nodeseek-auto-sign/multi_site_sign_simple.py
```

### 2. 获取Cookie

#### NodeSeek Cookie获取
1. 浏览器登录 [NodeSeek](https://www.nodeseek.com)
2. 按F12打开开发者工具
3. 切换到 `Network` 标签
4. 访问 [签到页面](https://www.nodeseek.com/board)
5. 在请求中找到Cookie值

#### DeepFlood Cookie获取
1. 浏览器登录 [DeepFlood](https://www.deepflood.com)
2. 按F12打开开发者工具
3. 切换到 `Network` 标签
4. 访问 [签到页面](https://www.deepflood.com/board)
5. 在请求中找到Cookie值

### 3. Telegram通知配置

#### 创建Telegram机器人
1. 在Telegram中搜索 `@BotFather`
2. 发送 `/newbot` 创建新机器人
3. 按提示设置机器人名称
4. 获得 `TG_BOT_TOKEN`

#### 获取用户ID
1. 在Telegram中搜索 `@userinfobot`
2. 发送任意消息获得你的 `TG_USER_ID`

## 🔧 配置说明

### 环境变量详解

| 变量名 | 必需 | 说明 | 示例 |
|--------|------|------|------|
| `NS_COOKIE` | ✅ | NodeSeek站点Cookie，多个用&分隔 | `cookie1&cookie2` |
| `DF_COOKIE` | ✅ | DeepFlood站点Cookie，多个用&分隔 | `cookie1&cookie2` |
| `TG_BOT_TOKEN` | ✅ | Telegram机器人Token | `1234567890:ABC...` |
| `TG_USER_ID` | ✅ | Telegram用户ID | `123456789` |
| `NS_USERNAMES` | ❌ | NodeSeek自定义用户名，多个用&分隔 | `张三&李四&王五` |
| `DF_USERNAMES` | ❌ | DeepFlood自定义用户名，多个用&分隔 | `用户A&用户B` |
| `NS_RANDOM` | ❌ | 随机参数，默认true | `true` |

### 用户名配置规则

#### 1. 顺序对应
用户名必须与Cookie顺序一一对应：
```bash
NS_COOKIE=cookie1&cookie2&cookie3
NS_USERNAMES=张三&李四&王五
#          ↑    ↑    ↑
#       cookie1→张三
#       cookie2→李四  
#       cookie3→王五
```

#### 2. 支持多种分隔符
```bash
NS_USERNAMES=张三&李四&王五    # & 分隔（推荐）
NS_USERNAMES=张三|李四|王五    # | 分隔
NS_USERNAMES=张三,李四,王五    # , 分隔
NS_USERNAMES=张三;李四;王五    # ; 分隔
```

#### 3. 部分配置
```bash
NS_COOKIE=cookie1&cookie2&cookie3&cookie4
NS_USERNAMES=张三&李四
# 结果显示：张三、李四、账号3、账号4
```

## 📱 通知效果

### 汇总通知示例
```
NodeSeek 签到汇总
成功: 3 个账号
失败: 0 个账号

张三: 签到成功，获得 5 个鸡腿
  近30天已签到25天，共获得125个鸡腿

李四: 签到成功，获得 3 个鸡腿
  近30天已签到23天，共获得98个鸡腿

王五: 签到成功，获得 4 个鸡腿
  近30天已签到20天，共获得80个鸡腿
```

### 通知优化
- ✅ **每天只发送一次** - 避免重复通知骚扰
- ✅ **汇总统计** - 显示成功/失败账号数量
- ✅ **详细信息** - 包含每个账号的签到结果和统计
- ✅ **分站点通知** - NodeSeek和DeepFlood分别发送

## 🐳 其他部署方式

### Docker部署
```bash
# 克隆仓库
git clone https://github.com/EmersonLopez2005/nodeseek-auto-sign.git
cd nodeseek-auto-sign

# 创建Cookie文件
mkdir cookie
echo "你的NodeSeek_Cookie" > cookie/NODESEEK_COOKIE.txt
echo "你的DeepFlood_Cookie" > cookie/DEEPFLOOD_COOKIE.txt

# 运行脚本
python3 multi_site_sign_simple.py
```

### GitHub Actions部署
1. Fork本仓库
2. 在仓库 `Settings` → `Secrets and variables` → `Actions` 中添加环境变量
3. 启用 GitHub Actions 工作流

## 📋 文件说明

```
nodeseek-auto-sign/
├── multi_site_sign_simple.py    # 主脚本（推荐使用）
├── notify.py                    # 通知模块
├── requirements.txt             # 依赖包列表
├── README.md                   # 使用说明
└── cookie/                     # Cookie存储目录（Docker用）
    ├── notification_status.json # 通知状态记录
    ├── NODESEEK_COOKIE.txt     # NodeSeek Cookie文件
    └── DEEPFLOOD_COOKIE.txt    # DeepFlood Cookie文件
```

## 🔍 常见问题

### Q: 为什么不支持账号密码登录？
A: 两个论坛都启用了Cloudflare机器人检测，账号密码登录成功率很低。Cookie登录更稳定可靠。

### Q: Cookie多久需要更新？
A: 通常Cookie有效期为1-3个月，失效后需要重新获取。脚本会自动检测Cookie失效并在通知中提醒。

### Q: 可以只使用其中一个站点吗？
A: 可以，只配置对应站点的Cookie即可。未配置的站点会自动跳过。

### Q: 通知发送失败怎么办？
A: 检查 `TG_BOT_TOKEN` 和 `TG_USER_ID` 是否正确，确保机器人已启动对话。

### Q: 签到失败怎么办？
A: 通常是Cookie失效导致，重新获取Cookie即可。也可能是网络问题，脚本会自动重试。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=EmersonLopez2005/nodeseek-auto-sign&type=Date)](https://star-history.com/#EmersonLopez2005/nodeseek-auto-sign&Date)

## 🙏 致谢

- 感谢 [NodeSeek](https://www.nodeseek.com) 和 [DeepFlood](https://www.deepflood.com) 提供优质的技术社区
- 感谢所有贡献者和用户的支持

---

如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！