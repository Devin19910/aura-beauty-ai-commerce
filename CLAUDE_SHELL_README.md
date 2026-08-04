# 🧠 Claude-Powered Intelligent Shell

A smart terminal interface where Claude AI helps you manage Project Athena directly from your shell!

---

## Quick Start

### 1. Set Your API Key
```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

### 2. Run the Shell
```bash
python claude-shell.py
```

### 3. Start Asking Questions!
```
athena> show me the current project status
athena> what agents do we have?
athena> explain the validation agent
athena> read backend/app/athena/agents/scoring_agent.py
athena> how do I run the dashboard?
athena> help
```

---

## What Claude Can Do

### 📁 File Operations
```
athena> read backend/app/athena/agents/research_agent.py
athena> list frontend/app/
athena> find "scoring_agent"
```

### 🔍 Project Analysis
```
athena> explain the 4-stage pipeline
athena> what's the architecture of Project Athena?
athena> show me how the API integrates with agents
athena> analyze the dashboard code
```

### 📊 Status & Monitoring
```
athena> status                    # Git status and recent commits
athena> tests                     # Run test suite
athena> dashboard                 # Check if dashboard is running
athena> api-health                # Check API health
```

### 🚀 Debugging & Help
```
athena> why is the dashboard not loading?
athena> how do I start the backend?
athena> what's wrong with the API?
athena> how do I deploy to production?
athena> suggest optimizations for the scoring agent
```

### 🛠️ Development Help
```
athena> how should I add a new agent?
athena> refactor this code: [paste code]
athena> write a test for the validation agent
athena> improve the dashboard performance
```

---

## Built-in Commands

| Command | Description |
|---------|-------------|
| `help` | Show all available commands |
| `status` | Show git status and recent commits |
| `tests` | Run all Project Athena tests |
| `logs` | View recent logs |
| `dashboard` | Check dashboard status |
| `api-health` | Check API health |
| `read <file>` | Read a file from project |
| `list <dir>` | List files in directory |
| `find <name>` | Search for files |
| `clear` | Clear the screen |
| `exit` | Exit the shell |

---

## Example Conversations

### Example 1: Understanding the System
```
athena> explain project athena in simple terms
Claude: Project Athena is a 4-stage AI pipeline that...
[Claude provides detailed explanation with file references]

athena> show me the research agent
Claude: Here's what the Research Agent does...
[Claude reads and explains the code]
```

### Example 2: Debugging
```
athena> the dashboard won't load
Claude: Let me check what might be wrong...
1. Is the frontend running? (npm run dev)
2. Is the API accessible? (http://localhost:8000)
3. Check the browser console for errors
[Claude provides troubleshooting steps]

athena> how do I start the frontend?
Claude: Run these commands:
cd frontend
npm install
npm run dev
```

### Example 3: Development
```
athena> read backend/app/athena/agents/scoring_agent.py
[Claude reads and shows the file]

athena> what can we improve in the scoring agent?
Claude: Here are optimization suggestions:
1. Cache trend calculations
2. Parallel supplier evaluation
3. Add progress logging
[Claude provides specific recommendations]
```

---

## Features

✅ **Smart Context Awareness**
- Claude knows your entire project structure
- Reads files on demand
- Understands agent architecture

✅ **Real-time Project Status**
- Git commit history
- File status
- Test results
- API health

✅ **Intelligent Assistance**
- Code analysis
- Debugging help
- Performance suggestions
- Documentation

✅ **Conversation History**
- Maintains context across multiple questions
- Remembers previous answers
- Builds on prior conversations

✅ **Beautiful Terminal Output**
- Color-coded responses
- Formatted code blocks
- Clean, readable interface

---

## Advanced Usage

### Multi-turn Conversations
Claude remembers context from previous messages:
```
athena> what is the scoring agent?
Claude: The Scoring Agent ranks products by opportunity...

athena> how does it calculate the composite score?
Claude: It uses a weighted formula...
[Claude references the previous context]

athena> can we improve it?
Claude: Yes, here are some ideas...
[Claude understands "it" refers to the scoring agent]
```

### Code Analysis
```
athena> read backend/app/athena/agents/validation_agent.py
[Shows the file]

athena> explain the validate function
Claude: The validate function checks...

athena> suggest optimizations
Claude: Here are improvements we could make...
```

### Debugging Workflow
```
athena> api-health
Claude: ✓ API is healthy

athena> tests
Claude: Shows test results

athena> why did test X fail?
Claude: Analyzes the failure and suggests fixes
```

---

## Requirements

- Python 3.8+
- Anthropic API key (get one at https://console.anthropic.com)
- Project Athena repository

## Installation

```bash
# API key already set up? Just run:
python claude-shell.py

# First time?
export ANTHROPIC_API_KEY=your-key
python claude-shell.py
```

---

## Tips & Tricks

1. **Ask about specific files**: "read backend/app/api/endpoints/athena.py"
2. **Get status**: Just type "status" for git info
3. **Run tests**: Type "tests" to see test results
4. **Long questions**: You can ask multi-line questions
5. **Clear context**: Type "clear" to reset the screen
6. **Exit anytime**: Type "exit" to quit

---

## Example Questions to Ask

```
"Explain the pipeline stages to me"
"How do the agents communicate?"
"What's in the dashboard?"
"Show me the API endpoints"
"How do I add a new agent?"
"What tests are failing?"
"How do I deploy this?"
"Suggest improvements for performance"
"Explain the validation agent logic"
"How does the scoring work?"
```

---

## Use Cases

### 🎓 Learning
Perfect for understanding Project Athena's architecture:
```
athena> walk me through how a product flows through the pipeline
```

### 🐛 Debugging
Get intelligent help finding and fixing issues:
```
athena> why isn't the API responding?
athena> my dashboard is blank, what's wrong?
```

### 📝 Development
Get code suggestions and improvements:
```
athena> how should I refactor this function?
athena> write a test for the supplier agent
```

### 📚 Documentation
Generate docs and explanations:
```
athena> create a README for the validation agent
athena> explain how the scoring algorithm works
```

---

## Keyboard Shortcuts

- `Ctrl+C`: Interrupt current response
- `Ctrl+D`: Exit (alternative to "exit")
- `↑/↓`: Access command history (if using enhanced shell)

---

## Troubleshooting

### "API key not set"
```bash
export ANTHROPIC_API_KEY=your-key
```

### "Cannot read file"
Make sure you're in the project root directory

### "API/Dashboard not responding"
Make sure backend/frontend are running:
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Claude Shell
python claude-shell.py
```

---

## What Makes This Special

🧠 **Claude is integrated into your development workflow**
- Not just answering questions
- Actually aware of your project structure
- Can read and analyze your code
- Understands Project Athena's architecture
- Provides contextualized help

This is like having an expert AI developer sitting next to you, ready to help with any Project Athena question!

---

## Next Level: Shell Aliases

Add to your `.bashrc` or `.zshrc`:
```bash
alias athena='python /path/to/claude-shell.py'
```

Then just type:
```bash
athena
```

---

## License & Credits

Built for Project Athena  
Powered by Claude AI  
Created with ❤️ for autonomous development

---

**Start exploring!** Type `python claude-shell.py` and begin your conversation with Claude. 🚀
