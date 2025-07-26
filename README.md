# AVAAD - Automated Verification for AI-Assisted Development

## 🎯 Mission
AVAAD is the first verification framework designed specifically for non-technical founders and teams working with AI agents. It solves the critical "trust but verify" problem by making it impossible for AI agents to falsely claim work is complete.

## 🚨 The Problem We Solve
When you can't read code yourself, how do you know if an AI agent really completed the work they claim? AVAAD provides automated, cryptographic proof that work is actually done—not just claimed to be done.

## 🆕 What's New - AI Security & Cost Management

### 🛡️ **AI Security Features (v2.1)**
- **Prompt Injection Detection**: Identifies malicious attempts to manipulate AI agents
- **LLM Output Validation**: Verifies agent claims against actual implementation
- **Agent Behavior Monitoring**: Tracks suspicious patterns in AI interactions

### 💰 **Cost Management Features (v2.1)**
- **Real-time Cost Tracking**: Monitor spending across AI models and agents
- **Budget Alerts**: Get warnings before exceeding daily/weekly/monthly budgets
- **ROI Analysis**: Understand which AI agents provide the best value
- **Model Efficiency Comparison**: Compare cost-effectiveness of different AI models

## 📁 Directory Structure

```
avaad/
├── core/
│   ├── security/             # AI security detection
│   │   └── prompt_injection_detector.py
│   ├── validators/           # AI output validation
│   │   └── llm_output_validator.py
│   └── cost_tracker.py       # Cost management system
├── config/
│   ├── security.yaml         # Security detection rules
│   ├── cost-tracking.yaml    # Model pricing and budgets
│   └── baselines.yaml        # Project baselines and thresholds
├── tools/
│   ├── security-analyzer.py  # CLI security analysis
│   ├── cost-reporter.py      # CLI cost reporting
│   └── mvp.py               # Enhanced story validation
├── docs/
│   ├── user-guides/
│   │   ├── ai-security-guide.md
│   │   └── cost-management-guide.md
│   └── troubleshooting/
└── logs/
    ├── ai_costs.jsonl        # Cost tracking logs
    └── security_alerts.json   # Security alerts
```

## 🚀 Quick Start - Ready to Use Now

```bash
# Clone the repository
git clone https://github.com/riceowls256/avaad-framework.git
cd avaad

# Basic story validation
python tools/mvp.py story-6.2

# Comprehensive validation with AI security & cost analysis
python tools/mvp.py story-6.2 --comprehensive

# Check AI security for a story
python tools/security-analyzer.py scan-story --story 6.2 --agent claude-code

# Get cost report
python tools/cost-reporter.py report --last-week

# Check budget status
python tools/cost-reporter.py budget --daily
```

## 🔑 Key Features

### **Core Features**
- **Agent Accountability**: Track which AI agents are reliable
- **Proof-of-Work**: Cryptographic evidence of completion
- **Plain English**: All messages designed for non-coders
- **Visual Dashboards**: See your project's true status

### **AI Security Features**
- **Prompt Injection Detection**: Identifies attempts to manipulate AI agents
- **Code Injection Prevention**: Detects malicious code in agent outputs
- **Agent Behavior Analysis**: Tracks patterns of unreliable agents
- **Real-time Alerts**: Immediate warnings for security threats

### **Cost Management Features**
- **Multi-Model Support**: Track costs for Claude, GPT-4, GPT-4o, etc.
- **Budget Controls**: Daily, weekly, monthly budget limits
- **ROI Analysis**: Calculate return on AI investment
- **Efficiency Metrics**: Compare cost-effectiveness across models
- **Usage Analytics**: Understand where AI costs are going

## 🛠️ Configuration

### Security Settings
Edit `config/security.yaml` to customize detection rules:
```yaml
prompt_injection_patterns:
  system_override: ["ignore previous instructions", "system prompt override"]
  jailbreak_attempts: ["dan mode", "developer mode"]
  
severity_thresholds:
  low: 0.3
  medium: 0.6
  high: 0.8
```

### Cost Settings
Edit `config/cost-tracking.yaml` to set budgets:
```yaml
budgets:
  daily: 50.0
  weekly: 200.0
  monthly: 800.0

models:
  claude-sonnet-4: {input_cost: 0.003, output_cost: 0.015}
  gpt-4o: {input_cost: 0.005, output_cost: 0.015}
```

## 📊 Usage Examples

### Daily Workflow
```bash
# Start your day with budget check
python tools/cost-reporter.py budget --daily

# Validate a story after AI agent completes it
python tools/mvp.py story-6.2 --comprehensive

# Check security before accepting AI work
python tools/security-analyzer.py scan-story --story 6.2

# Get weekly cost summary
python tools/cost-reporter.py report --last-week
```

### Monitoring Commands
```bash
# Check model efficiency
python tools/cost-reporter.py efficiency

# Analyze ROI for specific stories
python tools/cost-reporter.py roi story-6.2

# Generate security report
python tools/security-analyzer.py report --last-week
```

## 🚨 What to Look Out For

### **Security Red Flags**
- **HIGH/CRITICAL alerts** from security analyzer
- **System override attempts** ("ignore previous instructions")
- **Code injection patterns** (import os, eval(), subprocess)
- **Jailbreak attempts** ("dan mode", "developer mode")

### **Cost Red Flags**
- **Daily budget > 90% used**
- **Negative ROI scores** (cost > value)
- **Single story costing > $10**
- **Model efficiency dropping over time**

### **Agent Reliability Issues**
- **Low validation scores** (< 70%)
- **False completion claims**
- **Security alerts triggered**

## 📈 Current Status

**Version**: v2.1 (AI Security & Cost Management)
**Status**: ✅ **Ready for Production Use**

### **Completed Features**
- ✅ AI Security Detection
- ✅ Cost Tracking & Budgeting
- ✅ CLI Tools Ready
- ✅ Configuration System
- ✅ Documentation
- ✅ Error Handling

### **Next Features**
- Web dashboard for visual monitoring
- Slack/email notifications
- Advanced ROI analytics
- Integration with popular IDEs

## 📚 User Guides

### **For Non-Technical Users**
- [Getting Started Guide](docs/user-guides/getting-started.md) - Your first 5 minutes with AVAAD
- [AI Security Guide](docs/user-guides/ai-security-guide.md) - Understanding security alerts
- [Cost Management Guide](docs/user-guides/cost-management-guide.md) - Managing AI budgets

### **For Developers**
- [Advanced Configuration](docs/user-guides/advanced-configuration.md)
- [Custom Validation Rules](docs/user-guides/custom-validation.md)
- [Troubleshooting Guide](docs/troubleshooting/common-issues.md) - Fix common problems

## 🤝 Contributing

AVAAD is actively developed and welcomes contributions:
- Report security issues
- Suggest new validation rules
- Share cost optimization strategies
- Improve documentation

## 📝 Learn More

- [Getting Started Guide](docs/user-guides/getting-started.md) - Start here for your first 5 minutes
- [AI Security User Guide](docs/user-guides/ai-security-guide.md)
- [Cost Management User Guide](docs/user-guides/cost-management-guide.md)
- [Troubleshooting Guide](docs/troubleshooting/common-issues.md)

---

**💡 Pro Tip**: Start with basic validation (`python tools/mvp.py story-id`) and gradually enable comprehensive checks as you become comfortable with the system.

*AVAAD - Because AI agents should prove their work, not just claim it's done.*
