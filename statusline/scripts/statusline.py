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
    ctx_win = state.get("context_window", {})
    curr_usage = ctx_win.get("current_usage", {})
    
    uncached_tokens = curr_usage.get("input_tokens", 0)
    cached_prompt_tokens = curr_usage.get("cache_read_input_tokens", 0)
    completion_tokens = curr_usage.get("output_tokens", 0)
    
    total_prompt = uncached_tokens + cached_prompt_tokens
    hit_rate = (cached_prompt_tokens / total_prompt * 100) if total_prompt > 0 else 0.0
    
    ctx_usage = ctx_win.get("used_percentage", 0.0)
    
    line2 = (f"📈 未命中输入: {uncached_tokens} │ 🗂️ 缓存输入: {cached_prompt_tokens} │ "
             f"📤 输出: {completion_tokens} │ 🎯 命中率: {hit_rate:.1f}% │ 🧠 上下文使用: {ctx_usage:.1f}%")
             
    # ---------------------------------------------------------
    # ROW 3: Cost | Time | Plugin Ecosystem
    # ---------------------------------------------------------
    import time
    import tempfile
    
    # 1. Session Duration Tracking
    session_id = state.get("session_id", "unknown")
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
    
    # 2. Session Cost Estimation
    tot_input = ctx_win.get("total_input_tokens", 0)
    tot_output = ctx_win.get("total_output_tokens", 0)
    
    is_gemini = "Gemini" in model
    # Gemini 1.5 Pro est: $1.25/M input (blended), $5.00/M output
    # Opus est: $3.00/M input (blended), $15.00/M output
    if is_gemini:
        session_cost = (tot_input / 1000000) * 1.25 + (tot_output / 1000000) * 5.00
    else:
        session_cost = (tot_input / 1000000) * 3.00 + (tot_output / 1000000) * 15.00
        
    workspace_cost = 0.0000 # Requires persistent DB tracking, placeholder for now
    
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
