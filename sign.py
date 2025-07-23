#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NodeSeek 自动签到脚本（FlareSolverr 版）
- FlareSolverr 绕过 Cloudflare 5 秒盾
- 多账号、TG 推送
"""
import os
import re
import json
import time
import requests
from typing import List

# ========= 常量 =========
NS_LOGIN_URL = "https://www.nodeseek.com/auth/login"
NS_SIGN_URL  = "https://www.nodeseek.com/api/attendance"
FLARE_URL    = "http://localhost:8191/v1"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36")

# ========= 工具函数 =========
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

def flare_get(url: str) -> str:
    """
    用 FlareSolverr 绕过 CF，返回页面源码
    """
    payload = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": 60000
    }
    r = requests.post(FLARE_URL, json=payload, timeout=70).json()
    return r["solution"]["response"]

def flare_post(url: str, data: dict, cookie: str = "") -> dict:
    """
    用 FlareSolverr POST（携带 cookie）
    """
    headers = {
        "User-Agent": UA,
        "Referer": "https://www.nodeseek.com/board",
        "Origin": "https://www.nodeseek.com",
        "Content-Type": "application/json"
    }
    if cookie:
        headers["Cookie"] = cookie

    payload = {
        "cmd": "request.post",
        "url": url,
        "headers": headers,
        "postData": json.dumps(data, separators=(',', ':')),
        "maxTimeout": 60000
    }
    r = requests.post(FLARE_URL, json=payload, timeout=70).json()
    return json.loads(r["solution"]["response"] or "{}")

# ========= 登录 =========
def login(email: str, pwd: str) -> str:
    # 1. 拉登录页（已绕过 CF）
    html = flare_get(NS_LOGIN_URL)

    # 2. 提取 _token & sitekey
    token   = re.search(r'name="_token"\s+value="([^"]+)"', html)
    sitekey = re.search(r'data-sitekey="([^"]+)"', html)
    if not (token and sitekey):
        raise RuntimeError("未找到 token 或 sitekey")
    _token  = token.group(1)
    sitekey = sitekey.group(1)

    # 3. 本地 CloudFreed 破解
    cf_token = solve_turnstile(sitekey, NS_LOGIN_URL)
    if not cf_token:
        raise RuntimeError("验证码破解失败")

    # 4. 提交登录
    data = {
        "_token": _token,
        "email": email,
        "password": pwd,
        "cf-turnstile-response": cf_token
    }
    resp = flare_post(NS_LOGIN_URL, data)
    if "签到收益" not in json.dumps(resp):
        raise RuntimeError("登录失败，请检查账号密码/验证码")

    # 5. 返回 cookie（FlareSolverr 已带 cookie）
    return resp.get("cookie", "") or ""

# ========= 签到 =========
def sign(cookie: str, name: str) -> tuple:
    resp = flare_post(NS_SIGN_URL, {}, cookie)
    msg = resp.get("message", "unknown")
    return ("✅", msg) if "签到收益" in msg else ("❌", msg)

# ========= 主流程 =========
def main():
    results, success = [], 0
    idx = 1
    while True:
        email = os.getenv(f"USER{idx}")
        pwd   = os.getenv(f"PASS{idx}")
        if not email:
            break
        try:
            log(f"开始登录 {email}")
            cookie = login(email, pwd)
            flag, msg = sign(cookie, email)
            results.append(f"{flag} {email}：{msg}")
            if flag == "✅":
                success += 1
        except Exception as e:
            results.append(f"❌ {email}：{e}")
        idx += 1

    if not results:
        log("未配置任何账号")
        return

    summary = f"📋 NodeSeek 签到\n✅ 成功 {success} | ❌ {len(results)-success}\n" + "\n".join(results)
    log(summary)
    tg_notify(summary)

if __name__ == "__main__":
    main()
