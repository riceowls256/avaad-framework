# Getting Started with AVAAD

## 🚀 Quick Start (5 minutes)

### **Step 1: Clone and Setup**
```bash
# Clone the repository
git clone https://github.com/riceowls256/avaad-framework.git
cd avaad

# Make tools executable
chmod +x tools/*.py

# Test basic functionality
python tools/mvp.py --help
```

### **Step 2: Your First Validation**
```bash
# Validate a story (replace "6.2" with your actual story ID)
python tools/mvp.py 6.2

# Expected output: ✅ or ❌ with clear reasons
```

### **Step 3: Enable AI Security & Cost Tracking**
```bash
# Comprehensive validation with security & cost checks
python tools/mvp.py 6.2 --comprehensive

# Check security for a story
python tools/security-analyzer.py scan-story --story 6.2

# Check your AI costs
python tools/cost-reporter.py budget --daily
```

## 📋 Daily Workflow

### **Morning Routine (2 minutes)**
```bash
# 1. Check yesterday's costs
python tools/cost-reporter.py report --days 1

# 2. Check security summary
python tools/security-analyzer.py report --last-day

# 3. Validate completed stories
python tools/mvp.py story-id --comprehensive
```

### **After Each AI Agent Completes Work**
```bash
# 1. Validate the work actually got done
python tools/mvp.py story-6.2

# 2. Check for security issues
python tools/security-analyzer.py scan-story --story 6.2 --agent claude-code

# 3. Log the cost (if agent doesn't auto-log)
python tools/cost-reporter.py add-cost claude-sonnet-4 1500 300 --story 6.2 --description "Fixed login bug"
```

## 🎯 Understanding Your First Results

### **What Success Looks Like**
```
🔍 AVAAD Comprehensive Validation for Story 6.2
============================================================
📋 1. Checking practical functionality...
✅ Practical validation passed
🤖 2. Validating AI agent claims...
   AI Validation Score: 95.0%
   ✅ AI claims validated
🛡️ 3. Checking for security issues...
   ✅ No security issues detected
💰 4. Checking cost impact...
   AI Cost: $2.50
   ROI: 300.0%
   ✅ Cost-effective AI usage

🎉 Story validation complete!
✅ All checks passed - story is ready for completion
```

### **What Problems Look Like**
```
❌ Practical validation failed: Tests are failing
❌ Security issues detected: Code injection attempt
❌ Negative ROI - consider optimizing AI usage
```

## 🛠️ Setup for Your Project

### **1. Configure Your Budgets**
```bash
# Edit your budget limits
nano config/cost-tracking.yaml

# Example for small project:
budgets:
  daily: 10.0      # $10 per day max
  weekly: 50.0     # $50 per week max
  monthly: 200.0   # $200 per month max
```

### **2. Set Security Preferences**
```bash
# Customize security rules
nano config/security.yaml

# Common adjustments:
alerts:
  daily_warning: 8.0     # Alert at 80% of daily budget
  daily_critical: 9.0    # Critical alert at 90%
```

### **3. Update Project Baselines**
```bash
# Edit project-specific settings
nano config/baselines.yaml

# Set your project name and type
project:
  name: "your-project-name"
  type: "python-fastapi"
```

## 📊 Your First Week

### **Day 1-2: Learning**
- Run basic validation on 2-3 stories
- Check costs after each interaction
- Review security alerts (if any)

### **Day 3-4: Optimization**
- Adjust budgets based on actual usage
- Fine-tune security settings
- Compare AI model efficiency

### **Day 5-7: Mastery**
- Use comprehensive validation for all stories
- Weekly cost review
- Share findings with team

## 🎯 Common First Week Questions

### **"My costs seem high"**
```bash
# Check what you're spending on
python tools/cost-reporter.py efficiency

# Compare models
python tools/cost-reporter.py report --last-week --by-model
```

### **"Security alerts are scary"**
```bash
# Read the security guide
cat docs/user-guides/ai-security-guide.md

# Most alerts are informational - only HIGH/CRITICAL need action
```

### **"Validation is failing"**
```bash
# Check what's specifically failing
python tools/mvp.py story-6.2 --verbose

# Look at the troubleshooting guide
cat docs/troubleshooting/common-issues.md
```

## 🚀 Pro Tips for Success

### **Start Simple**
```bash
# Week 1: Just basic validation
python tools/mvp.py story-6.2

# Week 2: Add cost tracking
python tools/cost-reporter.py report --daily

# Week 3: Full security + cost + validation
python tools/mvp.py story-6.2 --comprehensive
```

### **Create Aliases**
```bash
# Add to your shell profile (~/.bashrc or ~/.zshrc)
echo 'alias avaad="python /path/to/avaad/tools/mvp.py"' >> ~/.zshrc
echo 'alias avaad-cost="python /path/to/avaad/tools/cost-reporter.py"' >> ~/.zshrc
echo 'alias avaad-security="python /path/to/avaad/tools/security-analyzer.py"' >> ~/.zshrc

# Then use:
avaad 6.2 --comprehensive
avaad-cost budget --daily
avaad-security report --last-week
```

### **Daily Command Cheat Sheet**
```bash
# Essential daily commands
python tools/mvp.py story-id           # Basic validation
python tools/mvp.py story-id --comprehensive  # Full checks
python tools/cost-reporter.py budget --daily  # Budget check
python tools/security-analyzer.py report --last-day  # Security summary
```

## 🎉 Your First Success

When you see this message:
```
🎉 Story validation complete!
✅ All checks passed - story is ready for completion
```

**You know:**
- ✅ The work is actually done
- ✅ No security issues
- ✅ Cost is reasonable
- ✅ ROI is positive

## 📞 Next Steps

### **After Your First Week:**
1. **Review** your cost patterns
2. **Adjust** budgets based on actual usage
3. **Share** the framework with your team
4. **Explore** advanced features

### **Advanced Features to Try:**
- Custom validation rules
- Team budget sharing
- Integration with CI/CD
- Custom security patterns

### **Getting Help:**
- Check [troubleshooting guide](../troubleshooting/common-issues.md)
- Read [security guide](ai-security-guide.md)
- Review [cost management guide](cost-management-guide.md)

---

**Remember:** Start with basic validation and gradually add features. The goal is to build trust in AI-assisted development, not to be perfect on day one!