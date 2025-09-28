# 自动签到脚本使用说明

## 脚本说明

我为你创建了三个脚本来解决你的问题：

1. **nodeseek_sign_improved.py** - 改进版综合脚本，支持NodeSeek和DeepFlood两个站点
2. **deepflood_sign.py** - 专门针对DeepFlood站点的独立脚本
3. **nodeseek_sign.py** - 你的原始脚本（保持不变）

## 主要改进

### 1. 解决Telegram通知频繁发送问题

**问题原因：**
- 原脚本每个账号签到后都会发送通知
- 登录失败时也会发送通知
- 没有通知去重机制

**解决方案：**
- 添加了通知状态管理，每天只发送一次汇总通知
- 使用JSON文件记录通知发送状态
- 汇总所有账号的签到结果后统一发送

### 2. 添加DeepFlood站点支持

- 新增DeepFlood站点配置
- 支持多站点统一管理
- 可以选择使用综合脚本或独立脚本

## 环境变量配置

### NodeSeek站点（原有配置保持不变）
```bash
# 单账号配置
USER=你的用户名
PASS=你的密码
NS_COOKIE=你的Cookie（可选，脚本会自动获取）

# 多账号配置
USER1=账号1用户名
PASS1=账号1密码
USER2=账号2用户名  
PASS2=账号2密码
# ... 以此类推

# 验证码相关
SOLVER_TYPE=turnstile  # 或 yescaptcha
API_BASE_URL=你的API地址
CLIENTT_KEY=你的客户端密钥
NS_RANDOM=true
```

### DeepFlood站点（新增配置）
```bash
# 单账号配置
DF_USER=你的DeepFlood用户名
DF_PASS=你的DeepFlood密码
DF_COOKIE=你的DeepFlood Cookie（可选）

# 多账号配置
DF_USER1=账号1用户名
DF_PASS1=账号1密码
DF_USER2=账号2用户名
DF_PASS2=账号2密码
# ... 以此类推
```

## 使用方式

### 方式1：使用综合脚本（推荐）
```bash
python nodeseek_sign_improved.py
```
这个脚本会同时处理NodeSeek和DeepFlood两个站点的签到。

### 方式2：使用独立脚本
```bash
# 只签到NodeSeek
python nodeseek_sign.py

# 只签到DeepFlood  
python deepflood_sign.py
```

## 青龙面板配置

### 1. 上传脚本
将脚本文件上传到青龙面板的脚本目录。

### 2. 配置环境变量
在青龙面板的环境变量中添加上述配置。

### 3. 添加定时任务
```bash
# 综合脚本（推荐）
30 8 * * * python3 /ql/scripts/nodeseek_sign_improved.py

# 或者分别运行
30 8 * * * python3 /ql/scripts/nodeseek_sign.py
35 8 * * * python3 /ql/scripts/deepflood_sign.py
```

## 通知优化说明

### 新的通知机制
1. **每日汇总**：每天只发送一次汇总通知，包含所有账号的签到结果
2. **状态记录**：使用JSON文件记录通知发送状态，避免重复发送
3. **详细信息**：通知包含签到成功/失败统计和详细的收益信息

### 通知内容示例
```
NodeSeek 签到汇总
成功: 2 个账号
失败: 0 个账号

账号1: 签到成功，获得 5 个鸡腿
  近30天已签到25天，共获得125个鸡腿

账号2: 签到成功，获得 3 个鸡腿  
  近30天已签到23天，共获得98个鸡腿
```

## 文件结构
```
NodeSeek-Signin-main/
├── nodeseek_sign.py              # 原始脚本
├── nodeseek_sign_improved.py     # 改进版综合脚本
├── deepflood_sign.py             # DeepFlood独立脚本
├── README.md                     # 使用说明
└── cookie/                       # Cookie和状态文件目录
    ├── NS_COOKIE.txt            # NodeSeek Cookie文件
    ├── DF_COOKIE.txt            # DeepFlood Cookie文件
    ├── notification_status.json  # 通知状态文件
    └── deepflood_notification_status.json
```

## 注意事项

1. **DeepFlood站点验证**：由于DeepFlood是新站点，可能需要调整sitekey等参数
2. **Cookie管理**：脚本会自动管理Cookie，无需手动更新
3. **通知频率**：现在每个站点每天只会发送一次汇总通知
4. **环境兼容**：支持青龙面板、Docker、GitHub Actions等多种环境

## 故障排除

### 如果DeepFlood登录失败
1. 检查sitekey是否正确（可能与NodeSeek不同）
2. 确认API接口地址是否正确
3. 检查验证码服务配置

### 如果通知仍然频繁发送
1. 检查cookie目录是否有写入权限
2. 确认通知状态文件是否正常创建
3. 可以手动删除状态文件重置通知状态

## 建议

1. **推荐使用综合脚本**：`nodeseek_sign_improved.py`可以同时处理两个站点
2. **测试新站点**：先用少量账号测试DeepFlood站点是否正常工作
3. **监控日志**：观察脚本运行日志，确保通知机制正常工作
4. **备份配置**：定期备份环境变量配置，避免丢失