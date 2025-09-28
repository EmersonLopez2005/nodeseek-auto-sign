# -*- coding: utf-8 -*-

import os
import time
import json
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from curl_cffi import requests

# ---------------- 通知模块动态加载 ----------------
hadsend = False
send = None
try:
    from notify import send
    hadsend = True
except ImportError:
    print("未加载通知模块，跳过通知功能")

# ---------------- 站点配置 ----------------
SITES_CONFIG = {
    "nodeseek": {
        "name": "NodeSeek",
        "sign_api": "https://www.nodeseek.com/api/attendance",
        "stats_api": "https://www.nodeseek.com/api/account/credit/page-",
        "board_url": "https://www.nodeseek.com/board",
        "origin": "https://www.nodeseek.com",
        "cookie_var": "NS_COOKIE",
        "username_var": "NS_USERNAMES"
    },
    "deepflood": {
        "name": "DeepFlood", 
        "sign_api": "https://www.deepflood.com/api/attendance",
        "stats_api": "https://www.deepflood.com/api/account/credit/page-",
        "board_url": "https://www.deepflood.com/board",
        "origin": "https://www.deepflood.com",
        "cookie_var": "DF_COOKIE",
        "username_var": "DF_USERNAMES"
    }
}

# ---------------- 通知状态管理 ----------------
NOTIFICATION_FILE = "./cookie/notification_status.json"

def load_notification_status():
    """加载通知状态"""
    try:
        if os.path.exists(NOTIFICATION_FILE):
            with open(NOTIFICATION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"加载通知状态失败: {e}")
    return {}

def save_notification_status(status):
    """保存通知状态"""
    try:
        os.makedirs(os.path.dirname(NOTIFICATION_FILE), exist_ok=True)
        with open(NOTIFICATION_FILE, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存通知状态失败: {e}")

def should_send_notification(site_name):
    """检查是否应该发送通知（每天只发送一次）"""
    status = load_notification_status()
    today = datetime.now().strftime('%Y-%m-%d')
    
    site_status = status.get(site_name, {})
    last_sent = site_status.get('last_sent_date')
    
    return last_sent != today

def mark_notification_sent(site_name):
    """标记通知已发送"""
    status = load_notification_status()
    today = datetime.now().strftime('%Y-%m-%d')
    
    if site_name not in status:
        status[site_name] = {}
    
    status[site_name]['last_sent_date'] = today
    save_notification_status(status)

# ---------------- 环境检测函数 ----------------
def detect_environment():
    """检测当前运行环境"""
    if os.environ.get("IN_DOCKER") == "true":
        return "docker"
        
    ql_path_markers = ['/ql/data/', '/ql/config/', '/ql/', '/.ql/']
    in_ql_env = False
    
    for path in ql_path_markers:
        if os.path.exists(path):
            in_ql_env = True
            break
    
    in_github_env = os.environ.get("GITHUB_ACTIONS") == "true" or (os.environ.get("GH_PAT") and os.environ.get("GITHUB_REPOSITORY"))
    
    if in_ql_env:
        return "qinglong"
    elif in_github_env:
        return "github"
    else:
        return "unknown"

# ---------------- Docker Cookie 文件读取 ----------------
def get_cookie_file_path(site_name):
    return f"./cookie/{site_name.upper()}_COOKIE.txt"

def load_cookies_from_file(site_name):
    """从文件加载Cookie"""
    try:
        cookie_file = get_cookie_file_path(site_name)
        if os.path.exists(cookie_file):
            with open(cookie_file, "r") as f:
                return f.read().strip()
    except Exception as e:
        print(f"从文件读取Cookie失败: {e}")
    return ""

# ---------------- 签到逻辑 ----------------
def sign(cookie, site_config, ns_random):
    if not cookie:
        return "invalid", "无有效Cookie"
        
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        'origin': site_config["origin"],
        'referer': site_config["board_url"],
        'Content-Type': 'application/json',
        'Cookie': cookie
    }
    try:
        url = f"{site_config['sign_api']}?random={ns_random}"
        response = requests.post(url, headers=headers, impersonate="chrome110")
        data = response.json()
        msg = data.get("message", "")
        if "鸡腿" in msg or data.get("success"):
            return "success", msg
        elif "已完成签到" in msg:
            return "already", msg
        elif data.get("status") == 404:
            return "invalid", msg
        return "fail", msg
    except Exception as e:
        return "error", str(e)

# ---------------- 查询签到收益统计函数 ----------------
def get_signin_stats(cookie, site_config, days=30):
    """查询前days天内的签到收益统计"""
    if not cookie:
        return None, "无有效Cookie"
    
    if days <= 0:
        days = 1
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        'origin': site_config["origin"],
        'referer': site_config["board_url"],
        'Cookie': cookie
    }
    
    try:
        shanghai_tz = ZoneInfo("Asia/Shanghai")
        now_shanghai = datetime.now(shanghai_tz)
        query_start_time = now_shanghai - timedelta(days=days)
        
        all_records = []
        page = 1
        
        while page <= 20:
            url = f"{site_config['stats_api']}{page}"
            response = requests.get(url, headers=headers, impersonate="chrome110")
            data = response.json()
            
            if not data.get("success") or not data.get("data"):
                break
                
            records = data.get("data", [])
            if not records:
                break
                
            last_record_time = datetime.fromisoformat(
                records[-1][3].replace('Z', '+00:00'))
            last_record_time_shanghai = last_record_time.astimezone(shanghai_tz)
            if last_record_time_shanghai < query_start_time:
                for record in records:
                    record_time = datetime.fromisoformat(
                        record[3].replace('Z', '+00:00'))
                    record_time_shanghai = record_time.astimezone(shanghai_tz)
                    if record_time_shanghai >= query_start_time:
                        all_records.append(record)
                break
            else:
                all_records.extend(records)
                
            page += 1
            time.sleep(0.5)
        
        signin_records = []
        for record in all_records:
            amount, balance, description, timestamp = record
            record_time = datetime.fromisoformat(
                timestamp.replace('Z', '+00:00'))
            record_time_shanghai = record_time.astimezone(shanghai_tz)
            
            if (record_time_shanghai >= query_start_time and
                    "签到收益" in description and "鸡腿" in description):
                signin_records.append({
                    'amount': amount,
                    'date': record_time_shanghai.strftime('%Y-%m-%d'),
                    'description': description
                })
        
        period_desc = f"近{days}天"
        if days == 1:
            period_desc = "今天"
        
        if not signin_records:
            return {
                'total_amount': 0,
                'average': 0,
                'days_count': 0,
                'records': [],
                'period': period_desc,
            }, f"查询成功，但没有找到{period_desc}的签到记录"
        
        total_amount = sum(record['amount'] for record in signin_records)
        days_count = len(signin_records)
        average = round(total_amount / days_count, 2) if days_count > 0 else 0
        
        stats = {
            'total_amount': total_amount,
            'average': average,
            'days_count': days_count,
            'records': signin_records,
            'period': period_desc
        }
        
        return stats, "查询成功"
        
    except Exception as e:
        return None, f"查询异常: {str(e)}"

# ---------------- 显示签到统计信息 ----------------
def print_signin_stats(stats, account_name):
    """打印签到统计信息"""
    if not stats:
        return
        
    print(f"\n==== {account_name} 签到收益统计 ({stats['period']}) ====")
    print(f"签到天数: {stats['days_count']} 天")
    print(f"总获得鸡腿: {stats['total_amount']} 个")
    print(f"平均每日鸡腿: {stats['average']} 个")

# ---------------- 解析用户名配置 ----------------
def parse_usernames(usernames_str):
    """解析用户名配置字符串"""
    if not usernames_str:
        return []
    
    # 支持多种分隔符：& | , ;
    usernames = re.split(r'[&|,;]', usernames_str)
    return [name.strip() for name in usernames if name.strip()]

# ---------------- 处理单个站点 ----------------
def process_site(site_name, site_config, ns_random):
    """处理单个站点的签到"""
    print(f"\n{'='*50}")
    print(f"开始处理 {site_config['name']} 站点")
    print(f"{'='*50}")
    
    env_type = detect_environment()
    
    # 读取Cookie
    all_cookies = ""
    if env_type == "docker":
        cookie_file = get_cookie_file_path(site_name)
        print(f"Docker环境，尝试从 {cookie_file} 读取Cookie...")
        all_cookies = load_cookies_from_file(site_name)
        if all_cookies:
            print("成功从文件加载Cookie。")
        else:
            print("Cookie文件不存在或为空。")
    else:
        all_cookies = os.getenv(site_config["cookie_var"], "")
        print(f"从环境变量 {site_config['cookie_var']} 读取Cookie")
        
    if not all_cookies:
        print(f"未找到 {site_config['name']} 的Cookie配置，跳过该站点")
        return
        
    cookie_list = all_cookies.split("&")
    cookie_list = [c.strip() for c in cookie_list if c.strip()]
    
    # 读取用户名配置
    usernames_str = os.getenv(site_config["username_var"], "")
    custom_usernames = parse_usernames(usernames_str)
    
    print(f"共发现 {len(cookie_list)} 个Cookie")
    if custom_usernames:
        print(f"发现 {len(custom_usernames)} 个自定义用户名: {custom_usernames}")
    
    site_results = []
    
    for i, cookie in enumerate(cookie_list):
        account_index = i + 1
        
        # 确定显示名称：优先使用自定义用户名，否则使用默认名称
        if i < len(custom_usernames):
            display_user = custom_usernames[i]
            print(f"\n==== {site_config['name']} {display_user} 开始签到 ====")
        else:
            display_user = f"账号{account_index}"
            print(f"\n==== {site_config['name']} {display_user} 开始签到 ====")
        
        result, msg = sign(cookie, site_config, ns_random)

        if result in ["success", "already"]:
            print(f"{display_user} 签到成功: {msg}")
            
            print("正在查询签到收益统计...")
            stats, stats_msg = get_signin_stats(cookie, site_config, 30)
            if stats:
                print_signin_stats(stats, display_user)
            else:
                print(f"统计查询失败: {stats_msg}")
            
            site_results.append({
                'account': display_user,
                'status': 'success',
                'message': msg,
                'stats': stats
            })
            
        else:
            print(f"{display_user} 签到失败: {msg}")
            site_results.append({
                'account': display_user,
                'status': 'failed',
                'message': msg,
                'stats': None
            })
    
    # 发送汇总通知（每天只发送一次）
    if hadsend and should_send_notification(site_name):
        try:
            success_count = len([r for r in site_results if r['status'] == 'success'])
            failed_count = len([r for r in site_results if r['status'] != 'success'])
            
            notification_msg = f"{site_config['name']} 签到汇总\n"
            notification_msg += f"成功: {success_count} 个账号\n"
            if failed_count > 0:
                notification_msg += f"失败: {failed_count} 个账号\n"
            
            # 添加成功账号的详细信息
            for result in site_results:
                if result['status'] == 'success':
                    notification_msg += f"\n{result['account']}: {result['message']}"
                    if result['stats']:
                        stats = result['stats']
                        notification_msg += f"\n  {stats['period']}已签到{stats['days_count']}天，共获得{stats['total_amount']}个鸡腿"
            
            # 添加失败账号信息
            for result in site_results:
                if result['status'] != 'success':
                    notification_msg += f"\n{result['account']}: {result['message']}"
            
            send(f"{site_config['name']} 签到汇总", notification_msg)
            mark_notification_sent(site_name)
            print(f"已发送 {site_config['name']} 汇总通知")
        except Exception as e:
            print(f"发送通知失败: {e}")

# ---------------- 主流程 ----------------
if __name__ == "__main__":
    ns_random = os.getenv("NS_RANDOM", "true")

    env_type = detect_environment()
    print(f"当前运行环境: {env_type}")
    print("Cookie多账户签到脚本启动")
    
    # 处理所有配置的站点
    for site_name, site_config in SITES_CONFIG.items():
        try:
            process_site(site_name, site_config, ns_random)
        except Exception as e:
            print(f"处理 {site_config['name']} 站点时发生异常: {e}")
    
    print(f"\n{'='*50}")
    print("所有站点处理完成")
    print(f"{'='*50}")
