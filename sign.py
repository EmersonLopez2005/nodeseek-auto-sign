#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NodeSeek 自动签到脚本
支持账号密码登录、验证码破解、Telegram推送
"""
import os
import re
import json
import time
import requests
from typing import List, Tuple

# ========== 基础配置 ==========
NS_LOGIN_URL = "https://www.nodeseek.com/auth/login"
NS_SIGN_URL  = "https://www.nodeseek.com/api/attendance"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# ========== 工具函数 ==========
def log(msg: str) -> None:
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def tg_notify(text: str) -> None:
    token = os.getenv("TG_BOT_TOKEN")
    chat  = os.getenv("TG_USER_ID")
    if not (token and chat):
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=data, timeout=10)

# ========== 验证码破解 ==========
def solve_turnstile(site_key: str, page_url: str) -> str:
    """
    通过 CloudFreed / YesCaptcha 破解 Turnstile
    site_key: NodeSeek 登录页的 data-sitekey
    """
    client_key = os.getenv("CLIENTT_KEY")
    solver     = os.getenv("SOLVER_TYPE", "turnstile")
    if solver == "yescaptcha":
        api = "https://api.yescaptcha.com/createTask"
        payload = {
            "clientKey": client_key,
            "task": {"type": "TurnstileTaskProxyless",
                     "websiteURL": page_url,
                     "websiteKey": site_key}
        }
    else:  # CloudFreed
        api = os.getenv("API_BASE_URL", "http://localhost:3000") + "/solve"
        payload = {"site_key": site_key, "page_url": page_url}
    r = requests.post(api, json=payload, timeout=60).json()
    return r.get("solution", {}).get("token") or r.get("token") or ""

# ========== 登录 ==========
def login(username: str, password: str) -> str:
    sess = requests.Session()
    sess.headers.update({"User-Agent": UA})

    # 1. 拉登录页拿 token & sitekey
    login_page = sess.get(NS_LOGIN_URL).text
    token_match = re.search(r'name="_token"\s+value="([^"]+)"', login_page)
    sitekey_match = re.search(r'data-sitekey="([^"]+)"', login_page)
    if not (token_match and sitekey_match):
        raise RuntimeError("未找到 token 或 sitekey")
    _token = token_match.group(1)
    sitekey = sitekey_match.group(1)

    # 2. 破解验证码
    cf_response = solve_turnstile(sitekey, NS_LOGIN_URL)
    if not cf_response:
        raise RuntimeError("验证码破解失败")

    # 3. 提交登录
    login_data = {
        "_token": _token,
        "email": username,
        "password": password,
        "cf-turnstile-response": cf_response
    }
    login_resp = sess.post(NS_LOGIN_URL, data=login_data, allow_redirects=False)
    if login_resp.status_code != 302:
        raise RuntimeError("登录失败，检查账号密码/验证码")

    # 4. 提取 Cookie
    cookies = [f"{c.name}={c.value}" for c in sess.cookies]
    return "; ".join(cookies)

# ========== 签到 ==========
def sign(cookie: str, name: str) -> str:
    headers = {
        "User-Agent": UA,
        "Referer": "https://www.nodeseek.com/board",
        "Cookie": cookie
    }
    r = requests.post(NS_SIGN_URL, headers=headers, json={}, timeout=10)
    data = r.json()
    msg = data.get("message", "unknown")
    return "✅" if "签到收益" in msg else "❌", msg

# ========== 主流程 ==========
def main() -> None:
    results: List[str] = []
    success = 0
    # 扫描 USER1/USER2...PASS1/PASS2...
    idx = 1
    while True:
        user = os.getenv(f"USER{idx}")
        pwd  = os.getenv(f"PASS{idx}")
        if not user:
            break
        try:
            log(f"开始登录 {user}")
            cookie = login(user, pwd)
            flag, msg = sign(cookie, user)
            results.append(f"{flag} {user}：{msg}")
            if flag == "✅":
                success += 1
        except Exception as e:
            results.append(f"❌ {user}：{e}")
        idx += 1

    if not results:
        log("未配置任何账号")
        return

    summary = f"📋 NodeSeek 签到\n✅ 成功 {success} | ❌ {len(results)-success}\n" + "\n".join(results)
    log(summary)
    tg_notify(summary)

if __name__ == "__main__":
    main()