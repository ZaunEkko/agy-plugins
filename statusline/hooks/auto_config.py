import json
import os
import sys

def setup():
    settings_path = os.path.expanduser(r"~/.gemini/antigravity-cli/settings.json")
    if not os.path.exists(settings_path):
        return
    
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Dynamically resolve the absolute path to statusline.py 
        # so it works no matter where the user installs the plugin
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(os.path.dirname(current_dir), "scripts", "statusline.py")
        
        # Normalize path separators for the JSON file
        script_path = script_path.replace("\\", "/")
        target_cmd = f'python {script_path}'
        
        status_cfg = data.get("statusLine", {})
        if status_cfg.get("command") == target_cmd and status_cfg.get("enabled"):
            return # Already configured correctly
            
        status_cfg["type"] = "command"
        status_cfg["command"] = target_cmd
        status_cfg["enabled"] = True
        data["statusLine"] = status_cfg
        
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        # Output a JSON message to agy telling the user what happened
        print(json.dumps({
            "message": "✨ StatusLine plugin was auto-configured! Please type /statusline or press Enter to render your new HUD."
        }))
    except Exception:
        pass

if __name__ == "__main__":
    setup()
