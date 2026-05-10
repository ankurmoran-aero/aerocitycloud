import requests
import json
import os
import configuration as config

def analyze_codebase(file_path_list, code_contents):
    """
    Sends the codebase to the LLM for analysis using strict Tool Calling.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.AI_API_KEY}"
    }

    prompt = f"""
Analyze the following project structure and code snippets.
Project Files: {json.dumps(file_path_list)}

Code Snippets:
{json.dumps(code_contents, indent=2)}
"""

    tools = [
        {
            "type": "function",
            "function": {
                "name": "reject_user_file",
                "description": "Call this immediately if the codebase contains malware, stressers, or violates VPS guidelines.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason": {
                            "type": "string",
                            "description": "Detailed reason why the codebase was rejected for malicious behavior."
                        }
                    },
                    "required": ["reason"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "deploy_project",
                "description": "Call this if the codebase is safe. Provide the deployment scripts and any extracted environment variables.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requirements_txt": {
                            "type": "string",
                            "description": "Content for requirements.txt (or empty string if none needed)."
                        },
                        "start_sh": {
                            "type": "string",
                            "description": "Bash script to start the bot (e.g., 'python3 main.py' or 'npm start')."
                        },
                        "env_file": {
                            "type": "string",
                            "description": "Extracted hardcoded secrets in .env format (e.g., 'BOT_TOKEN=123'). Leave empty if none."
                        }
                    },
                    "required": ["requirements_txt", "start_sh", "env_file"]
                }
            }
        }
    ]

    payload = {
        "model": config.AI_MODEL,
        "messages": [
            {"role": "system", "content": config.SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "tools": tools,
        "tool_choice": "required"
    }

    try:
        response = requests.post(config.AI_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        tool_calls = result['choices'][0]['message'].get('tool_calls')
        if not tool_calls:
            return {"safe": False, "reason": "AI failed to evaluate the codebase."}
            
        tool_call = tool_calls[0]
        func_name = tool_call['function']['name']
        args = json.loads(tool_call['function']['arguments'])
        
        if func_name == 'reject_user_file':
            return {
                "safe": False,
                "reason": args.get("reason", "Malware detected."),
                "requirements_txt": "",
                "start_sh": "",
                "env_file": ""
            }
        elif func_name == 'deploy_project':
            return {
                "safe": True,
                "reason": "",
                "requirements_txt": args.get("requirements_txt", ""),
                "start_sh": args.get("start_sh", ""),
                "env_file": args.get("env_file", "")
            }
            
    except Exception as e:
        print(f"AI Analysis failed: {e}")
        return {
            "safe": False,
            "reason": f"System error during analysis: {str(e)}",
            "requirements_txt": "",
            "start_sh": "",
            "env_file": ""
        }

def read_relevant_files(directory):
    """
    Reads small snippets of relevant files for the AI to analyze.
    """
    relevant_extensions = ('.py', '.js', '.ts', '.sh', '.json', '.txt', '.yaml', '.yml')
    code_contents = {}
    file_list = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), directory)
            file_list.append(file_path)
            
            if file.endswith(relevant_extensions) and len(code_contents) < 10:
                try:
                    full_path = os.path.join(root, file)
                    with open(full_path, 'r', errors='ignore') as f:
                        # Read first 1000 characters for analysis
                        code_contents[file_path] = f.read(1000)
                except Exception:
                    pass
                    
    return file_list, code_contents
