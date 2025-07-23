# nodeseek-auto-sign
nodeseek-auto-sign
青龙面板环境变量（系统 → 环境变量）
| 变量名            | 示例值                         |
| -------------- | --------------------------- |
| `USER1`        | `alice@example.com`         |
| `PASS1`        | `mySecretPwd`               |
| `CLIENTT_KEY`  | `abc123xyz`                 |
| `SOLVER_TYPE`  | `turnstile`                 |
| `API_BASE_URL` | `http://192.168.1.100:3000` |
⚠️ 注意事项
变量名大小写必须一致，否则脚本读不到。
只有账号密码必填，其余按需填写即可。
多账号继续加 USER3/PASS3 … 以此类推。
