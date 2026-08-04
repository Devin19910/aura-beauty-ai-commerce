#!/usr/bin/env python3
"""
Claude-Powered Intelligent Shell for Project Athena
An interactive terminal where Claude AI helps manage your project
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import anthropic

# Configuration
PROJECT_ROOT = Path(__file__).parent
CLAUDE_MODEL = "claude-opus-5"
API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not API_KEY:
    print("❌ Error: ANTHROPIC_API_KEY not set")
    print("Set it with: export ANTHROPIC_API_KEY=your-key")
    sys.exit(1)

client = anthropic.Anthropic(api_key=API_KEY)

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header():
    """Print shell header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       🧠 CLAUDE-POWERED PROJECT ATHENA SHELL 🧠           ║")
    print("║       Intelligent AI Assistant for Your Project             ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    print(f"{Colors.BLUE}Type 'help' for commands | 'exit' to quit{Colors.ENDC}\n")


def get_project_context() -> str:
    """Gather project context for Claude"""
    context = f"""
# Project Athena - Current Context
- Location: {PROJECT_ROOT}
- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Project Structure
"""

    # Add key directories
    for item in ["backend", "frontend", "tests"]:
        path = PROJECT_ROOT / item
        if path.exists():
            files = list(path.rglob("*.py"))[:5]  # Limit to 5 files per dir
            context += f"\n- {item}/: {len(list(path.rglob('*')))} files"

    # Add status of key files
    key_files = [
        "backend/app/athena/agents/research_agent.py",
        "backend/app/athena/agents/supplier_agent.py",
        "backend/app/athena/agents/validation_agent.py",
        "backend/app/athena/agents/scoring_agent.py",
        "backend/app/api/endpoints/athena.py",
        "frontend/app/dashboard/page.tsx",
    ]

    context += "\n\n## Key Files Status\n"
    for file_path in key_files:
        full_path = PROJECT_ROOT / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            context += f"✓ {file_path} ({size} bytes)\n"
        else:
            context += f"✗ {file_path} (missing)\n"

    # Add git status if available
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            changes = result.stdout.strip()
            context += f"\n## Git Status\n{changes if changes else '(Clean working directory)'}\n"
    except:
        pass

    return context


def read_file_safe(file_path: str) -> str:
    """Safely read a file from the project"""
    try:
        full_path = PROJECT_ROOT / file_path
        if not full_path.exists():
            return f"File not found: {file_path}"

        # Limit file size to avoid huge context
        if full_path.stat().st_size > 50000:
            return f"File too large: {file_path} (limit: 50KB)"

        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def execute_command(cmd: str) -> str:
    """Execute a shell command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=PROJECT_ROOT
        )
        output = result.stdout + result.stderr
        return output[:2000] if len(output) > 2000 else output
    except subprocess.TimeoutExpired:
        return "Command timed out (10s limit)"
    except Exception as e:
        return f"Error executing command: {str(e)}"


def format_claude_response(text: str) -> str:
    """Format Claude's response with colors"""
    # Add colors to different parts
    text = text.replace("✓", f"{Colors.GREEN}✓{Colors.ENDC}")
    text = text.replace("✗", f"{Colors.RED}✗{Colors.ENDC}")
    text = text.replace("⚠", f"{Colors.YELLOW}⚠{Colors.ENDC}")

    # Bold headers
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        if line.startswith('#') or line.startswith('##'):
            formatted_lines.append(f"{Colors.BOLD}{line}{Colors.ENDC}")
        elif line.startswith('-') or line.startswith('•'):
            formatted_lines.append(f"{Colors.CYAN}{line}{Colors.ENDC}")
        else:
            formatted_lines.append(line)

    return '\n'.join(formatted_lines)


def build_system_prompt() -> str:
    """Build the system prompt for Claude"""
    return """You are Claude, an expert AI assistant deeply integrated into the Project Athena development environment.

You have full knowledge of:
- Project Athena: 4-stage autonomous product intelligence pipeline
- Backend (FastAPI): Research, Supplier, Validation, Scoring agents
- Frontend (Next.js): Live monitoring dashboard
- APIs: 8 REST endpoints for workflow management
- Technologies: Python, FastAPI, PostgreSQL, Redis, Next.js, React

Your capabilities:
✓ Read and analyze project files
✓ Explain code and architecture
✓ Suggest improvements and optimizations
✓ Help debug issues
✓ Manage Project Athena workflows
✓ Execute shell commands
✓ Monitor system status
✓ Generate documentation

When users ask questions:
1. Provide clear, concise answers
2. Reference specific files/code when relevant
3. Use code blocks for examples
4. Suggest actionable improvements
5. Explain your reasoning

Always be helpful, accurate, and focused on Project Athena's goals."""


def chat_with_claude(user_input: str, conversation_history: list) -> str:
    """Send message to Claude and get response"""

    # Build the messages for Claude
    messages = conversation_history.copy()

    # Add current user message
    messages.append({
        "role": "user",
        "content": user_input
    })

    # Get project context
    context = get_project_context()

    # Enhance the prompt with project context
    enhanced_message = f"""
{context}

---

User Request: {user_input}

Please help with this request. If the user asks to read a file, check if it's in the project first.
"""

    # Update the last message with enhanced content
    messages[-1]["content"] = enhanced_message

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2048,
            system=build_system_prompt(),
            messages=messages
        )

        return response.content[0].text
    except Exception as e:
        return f"❌ Error communicating with Claude: {str(e)}"


def process_special_commands(user_input: str) -> tuple[bool, str]:
    """Process special shell commands"""

    if user_input.lower() == "help":
        help_text = f"""{Colors.BOLD}Available Commands:{Colors.ENDC}

{Colors.GREEN}Project Commands:{Colors.ENDC}
  status          - Show project status and recent changes
  tests           - Run test suite
  logs            - View recent logs
  agents          - Show agent status

{Colors.GREEN}File Operations:{Colors.ENDC}
  read <file>     - Read a file from the project
  list <dir>      - List files in a directory
  find <name>     - Search for files by name

{Colors.GREEN}Dashboard:{Colors.ENDC}
  dashboard       - Check dashboard status
  api-health      - Check API health

{Colors.GREEN}Utilities:{Colors.ENDC}
  clear           - Clear screen
  exit            - Exit the shell
  help            - Show this help message

{Colors.YELLOW}Or just ask Claude anything about your project!{Colors.ENDC}
"""
        return True, help_text

    elif user_input.lower() == "clear":
        os.system("clear" if os.name == "posix" else "cls")
        return True, ""

    elif user_input.lower() == "status":
        cmd = "git log --oneline -5 && git status --short"
        output = execute_command(cmd)
        return True, f"Recent commits and changes:\n{output}"

    elif user_input.lower() == "tests":
        output = execute_command("python -m pytest backend/app/athena/test_*.py -v --tb=short 2>&1 | tail -20")
        return True, f"Test results:\n{output}"

    elif user_input.lower().startswith("read "):
        file_path = user_input[5:].strip()
        content = read_file_safe(file_path)
        return True, f"Content of {file_path}:\n\n{content[:1500]}"

    elif user_input.lower() == "dashboard":
        output = execute_command("curl -s http://localhost:3000/dashboard 2>&1 | head -5")
        if "refused" in output.lower():
            return True, "⚠ Dashboard not running. Start it with: npm run dev (in frontend directory)"
        return True, "✓ Dashboard is accessible at http://localhost:3000/dashboard"

    elif user_input.lower() == "api-health":
        output = execute_command("curl -s http://localhost:8000/api/v1/athena/health 2>&1")
        return True, f"API Health Check:\n{output}"

    return False, ""


def main():
    """Main shell loop"""
    print_header()

    conversation_history = []

    while True:
        try:
            # Get user input
            user_input = input(f"{Colors.BOLD}athena> {Colors.ENDC}").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print(f"\n{Colors.CYAN}Goodbye! Keep building amazing things.{Colors.ENDC}\n")
                break

            # Check for special commands
            is_special, response = process_special_commands(user_input)

            if is_special:
                if response:
                    print(f"\n{Colors.GREEN}{response}{Colors.ENDC}\n")
                continue

            # Send to Claude
            print(f"\n{Colors.BLUE}Claude is thinking...{Colors.ENDC}")
            response = chat_with_claude(user_input, conversation_history)

            # Format and display response
            formatted_response = format_claude_response(response)
            print(f"\n{Colors.GREEN}{formatted_response}{Colors.ENDC}\n")

            # Update conversation history
            conversation_history.append({
                "role": "user",
                "content": user_input
            })
            conversation_history.append({
                "role": "assistant",
                "content": response
            })

            # Keep conversation history manageable
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Interrupted. Type 'exit' to quit.{Colors.ENDC}\n")
        except Exception as e:
            print(f"\n{Colors.RED}Error: {str(e)}{Colors.ENDC}\n")


if __name__ == "__main__":
    main()
