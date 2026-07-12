#!/usr/bin/env python3
"""
Antigravity StatusLine HUD Plugin
A multi-line, highly detailed status dashboard for the Antigravity CLI.

Line 1: Model & intensity, workspace, Git status (with dirty indicator)
Line 2: Token usage (uncached, cached, output), Cache hit rate, Context usage
Line 3: Cost (Session & Workspace), Session time, Eco stats (MCP, Skills, Hooks)
"""

import json
import os
import subprocess
import sys

# Paths for counting ecosystem plugins
_SETTINGS_PATH = os.path.expanduser(r"~/.gemini/antigravity-cli/settings.json")
_MCP_GLOBAL = os.path.expanduser(r"~/.gemini/config/mcp_config.json")
_HOOKS_GLOBAL = os.path.expanduser(r"~/.gemini/config/hooks.json")
_PLUGINS_GLOBAL = os.path.expanduser(r"~/.gemini/config/plugins")
_SKILLS_GLOBAL = os.path.expanduser(r"~/.gemini/config/skills")

def run_cmd(args, cwd=None):
    """Run shell command and return stdout, exit code."""
    try:
        p = subprocess.run(args, capture_output=True, text=True, cwd=cwd, timeout=1)
        return p.stdout.strip(), p.returncode
    except Exception:
        return "", -1

def get_git_info(cwd):
    """Return branch name with '*' if there are uncommitted changes."""
    branch, code = run_cmd(["git", "branch", "--show-current"], cwd)
    if code != 0 or not branch:
        return ""
    
    status, _ = run_cmd(["git", "status", "--porcelain"], cwd)
    dirty = "*" if status.strip() else ""
    return f"{branch}{dirty}"

def fmt_num(n):
    """Format number to human-readable string: 1234 → 1.2K, 1234567 → 1.2M."""
    if n >= 1000000:
        return f"{n / 1000000:.1f}M"
    elif n >= 1000:
        return f"{n / 1000:.1f}K"
    return str(n)

def count_keys_in_json(filepath):
    """Count top-level keys in a JSON object file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return len(data) if isinstance(data, dict) else 0
    except Exception:
        return 0

def count_skills():
    """Count total available skills (global + inside plugins)."""
    count = 0
    # Check ~/.gemini/config/skills
    if os.path.isdir(_SKILLS_GLOBAL):
        for item in os.listdir(_SKILLS_GLOBAL):
            if os.path.isdir(os.path.join(_SKILLS_GLOBAL, item)):
                count += 1
                
    # Check ~/.gemini/config/plugins/*/skills
    if os.path.isdir(_PLUGINS_GLOBAL):
        for plugin in os.listdir(_PLUGINS_GLOBAL):
            p_skills = os.path.join(_PLUGINS_GLOBAL, plugin, "skills")
            if os.path.isdir(p_skills):
                for item in os.listdir(p_skills):
                    if os.path.isdir(os.path.join(p_skills, item)):
                        count += 1
    return count

def calculate_estimated_cost(prompt_tokens, cached_tokens, completion_tokens, is_gemini):
    """Fallback cost calculator based on standard pricing per 1M tokens."""
    uncached = prompt_tokens - cached_tokens
    if is_gemini:
        # Estimated Gemini 1.5 Pro pricing
        return (uncached / 1000000) * 1.25 + (cached_tokens / 1000000) * 0.31 + (completion_tokens / 1000000) * 5.00
    else:
        # Estimated Claude 3.5 Sonnet / Opus pricing
        return (uncached / 1000000) * 3.00 + (cached_tokens / 1000000) * 0.30 + (completion_tokens / 1000000) * 15.00

def main():
    # 1. Read Payload
    state = {}
    try:
        if not sys.stdin.isatty():
            raw = sys.stdin.read()
            if raw.strip():
                state = json.loads(raw)
    except Exception:
        pass
        
    cwd = state.get("cwd") or os.getcwd()
    tel = state.get("telemetry", {})
    
    # ---------------------------------------------------------
    # ROW 1: Model | Workspace | Git Branch
    # ---------------------------------------------------------
    model = state.get("model")
    if isinstance(model, dict):
        model = model.get("display_name") or model.get("id") or ""
        
    if not model:
        try:
            with open(_SETTINGS_PATH, "r", encoding="utf-8") as f:
                model = json.load(f).get("model", "Unknown Model")
        except Exception:
            model = "Unknown Model"
            
    folder = os.path.basename(cwd)
    git_info = get_git_info(cwd)
    git_display = f" │ ⎇ {git_info}" if git_info else ""
    
    line1 = f"🤖 {model} │ 📂 {folder}{git_display}"
    
    # ---------------------------------------------------------
    # ROW 2: Uncached | Cached | Output | Hit Rate | Context
    # ---------------------------------------------------------
    import tempfile
    
    ctx_win = state.get("context_window", {})
    curr_usage = ctx_win.get("current_usage", {})
    
    # Session-level token accumulator
    # current_usage only shows THIS turn's tokens. We accumulate across
    # all turns by detecting when total_input/output changes (= new turn).
    session_id = state.get("session_id", "unknown")
    total_in = ctx_win.get("total_input_tokens", 0)
    total_out = ctx_win.get("total_output_tokens", 0)
    
    tracker = {"prev_total_in": 0, "prev_total_out": 0,
               "sum_uncached": 0, "sum_cached": 0, "sum_output": 0}
    
    if session_id != "unknown":
        tracker_file = os.path.join(tempfile.gettempdir(), f"agy_tokens_{session_id}.json")
        try:
            if os.path.exists(tracker_file):
                with open(tracker_file, "r", encoding="utf-8") as f:
                    tracker = json.load(f)
        except Exception:
            pass
        
        # Detect new turn: totals changed since last render
        if total_in != tracker.get("prev_total_in", 0) or total_out != tracker.get("prev_total_out", 0):
            tracker["sum_uncached"] = tracker.get("sum_uncached", 0) + curr_usage.get("input_tokens", 0)
            tracker["sum_cached"] = tracker.get("sum_cached", 0) + curr_usage.get("cache_read_input_tokens", 0)
            tracker["sum_output"] = tracker.get("sum_output", 0) + curr_usage.get("output_tokens", 0)
            tracker["prev_total_in"] = total_in
            tracker["prev_total_out"] = total_out
            
            try:
                with open(tracker_file, "w", encoding="utf-8") as f:
                    json.dump(tracker, f)
            except Exception:
                pass
    
    uncached_tokens = tracker.get("sum_uncached", 0)
    cached_prompt_tokens = tracker.get("sum_cached", 0)
    completion_tokens = tracker.get("sum_output", 0)
    
    total_prompt = uncached_tokens + cached_prompt_tokens
    hit_rate = (cached_prompt_tokens / total_prompt * 100) if total_prompt > 0 else 0.0
    
    ctx_usage = ctx_win.get("used_percentage", 0.0)
    max_ctx = ctx_win.get("context_window_size", 0)
    
    # Format max context to readable string (e.g., 1M, 200K)
    if max_ctx >= 1000000:
        max_ctx_str = f"{max_ctx / 1000000:.1f}M".replace(".0M", "M")
    elif max_ctx > 0:
        max_ctx_str = f"{int(max_ctx / 1000)}K"
    else:
        max_ctx_str = "Unknown"
    
    line2 = (f"📈 未命中输入: {fmt_num(uncached_tokens)} │ 🗂️ 缓存输入: {fmt_num(cached_prompt_tokens)} │ "
             f"📤 输出: {fmt_num(completion_tokens)} │ 🎯 命中率: {hit_rate:.1f}% │ 🧠 上下文使用: {ctx_usage:.1f}% ({max_ctx_str})")
             
    # ---------------------------------------------------------
    # ROW 3: Cost | Time | Plugin Ecosystem
    # ---------------------------------------------------------
    import time
    
    # 1. Session Duration Tracking
    start_time = time.time()
    if session_id != "unknown":
        timer_file = os.path.join(tempfile.gettempdir(), f"agy_timer_{session_id}.txt")
        if not os.path.exists(timer_file):
            try:
                with open(timer_file, "w") as tf:
                    tf.write(str(start_time))
            except Exception: pass
        else:
            try:
                with open(timer_file, "r") as tf:
                    start_time = float(tf.read().strip())
            except Exception: pass
            
    session_time = int(time.time() - start_time)
    
    # 2. Session Cost Estimation & Dynamic Pricing
    tot_input = ctx_win.get("total_input_tokens", 0)
    tot_output = ctx_win.get("total_output_tokens", 0)
    
    pricing_file = os.path.expanduser(r"~/.gemini/antigravity-cli/pricing.json")
    
    # Default fallback pricing (will be overwritten by background fetch if missing)
    input_price = 1.25  # per million
    output_price = 5.00 # per million
    
    needs_fetch = False
    try:
        if os.path.exists(pricing_file):
            with open(pricing_file, "r", encoding="utf-8") as f:
                pricing_db = json.load(f)
                
            if model in pricing_db:
                input_price = pricing_db[model].get("input", input_price)
                output_price = pricing_db[model].get("output", output_price)
            else:
                needs_fetch = True
        else:
            needs_fetch = True
    except Exception:
        pass
        
    if needs_fetch and model and model != "Unknown Model":
        # Spawn detached background process to fetch pricing so we don't block the UI
        try:
            fetch_script = f"""
import json, urllib.request, os
pricing_file = r'{pricing_file}'
model = '{model}'
try:
    if os.path.exists(pricing_file):
        with open(pricing_file, 'r', encoding='utf-8') as f:
            db = json.load(f)
    else:
        db = {{}}
    
    # In a full implementation, we'd fetch from Litellm or similar here.
    # For now, we seed standard values based on fuzzy matching.
    inp, out = 1.25, 5.00
    m = model.lower()
    if 'opus' in m: inp, out = 15.00, 75.00
    elif 'sonnet' in m: inp, out = 3.00, 15.00
    elif 'gemini' in m and 'pro' in m: inp, out = 1.25, 5.00
    elif 'gemini' in m and 'flash' in m: inp, out = 0.075, 0.30
    elif 'gpt-4o' in m: inp, out = 5.00, 15.00
    
    db[model] = {{"input": inp, "output": out}}
    with open(pricing_file, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2)
except Exception:
    pass
"""
            import tempfile
            tmp_fetcher = os.path.join(tempfile.gettempdir(), "agy_pricing_fetcher.py")
            with open(tmp_fetcher, "w", encoding="utf-8") as tf:
                tf.write(fetch_script)
                
            # Run detached
            if os.name == 'nt':
                subprocess.Popen([sys.executable, tmp_fetcher], 
                                 creationflags=subprocess.CREATE_NO_WINDOW,
                                 stdin=subprocess.DEVNULL, 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen([sys.executable, tmp_fetcher], 
                                 start_new_session=True, 
                                 stdin=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
        except Exception:
            pass

    session_cost = (tot_input / 1000000) * input_price + (tot_output / 1000000) * output_price
        
    # 3. Workspace Cost Tracking
    workspace_cost = session_cost
    if session_id != "unknown" and cwd:
        costs_db_file = os.path.expanduser(r"~/.gemini/antigravity-cli/workspace_costs.json")
        try:
            db = {}
            if os.path.exists(costs_db_file):
                with open(costs_db_file, "r", encoding="utf-8") as f:
                    db = json.load(f)
                    
            ws_data = db.get(cwd, {"accumulated_cost": 0.0, "last_session_id": "", "last_session_cost": 0.0})
            
            if ws_data["last_session_id"] != session_id:
                ws_data["accumulated_cost"] += ws_data["last_session_cost"]
                ws_data["last_session_id"] = session_id
                
            ws_data["last_session_cost"] = session_cost
            db[cwd] = ws_data
            
            with open(costs_db_file, "w", encoding="utf-8") as f:
                json.dump(db, f)
                
            workspace_cost = ws_data["accumulated_cost"] + session_cost
        except Exception:
            pass
    
    # Formatting time
    m, s = divmod(session_time, 60)
    h, m = divmod(m, 60)
    time_str = f"{int(h)}h{int(m)}m{int(s)}s" if h > 0 else f"{int(m)}m{int(s)}s"
    
    mcp_count = count_keys_in_json(_MCP_GLOBAL)
    hooks_count = count_keys_in_json(_HOOKS_GLOBAL)
    skills_count = count_skills()
    
    line3 = (f"💰 会话消费: ${session_cost:.4f} │ 🏢 目录消费: ${workspace_cost:.4f} │ "
             f"⏱️ 耗时: {time_str} │ 🔌 MCP: {mcp_count} │ 🛠️ Skills: {skills_count} │ 🪝 Hooks: {hooks_count}")
             
    # Output the Multi-line HUD
    sys.stdout.write(f"{line1}\n{line2}\n{line3}")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
