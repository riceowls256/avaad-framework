# Common Issues & Troubleshooting

## 🚨 Quick Fix Commands

### "Module not found" errors
```bash
# Fix import issues
export PYTHONPATH="/Users/Shared/Tech/Projects/BMAD_projects/avaad:$PYTHONPATH"
python tools/mvp.py story-6.2
```

### "Config file not found" errors
```bash
# Check config files exist
ls -la config/
# Should show: baselines.yaml, cost-tracking.yaml, security.yaml
```

### "Permission denied" errors
```bash
# Make tools executable
chmod +x tools/*.py
python tools/mvp.py story-6.2
```

## 🔧 Common Problems & Solutions

### **Problem: Security analyzer shows no agent interactions**
**Symptoms:**
```
⚠️ No agent interactions found for security check
```

**Solution:**
1. Ensure your AI agent is logging interactions
2. Check `logs/` directory for interaction files
3. Create sample interaction file if needed:
```bash
# Create a sample interaction log
echo '{"timestamp": "2025-07-26T10:00:00Z", "agent": "claude-code", "prompt": "fix bug", "response": "fixed bug"}' > logs/story-6.2-interactions.json
```

### **Problem: Cost reporter shows no data**
**Symptoms:**
```
No cost data found for period
```

**Solution:**
1. Start logging costs manually:
```bash
python tools/cost-reporter.py add-cost claude-sonnet-4 1000 200 --story 6.2 --description "Initial test"
```

2. Check logs directory:
```bash
ls -la logs/ai_costs.jsonl
```

### **Problem: MVP validation fails with "No agent output found"**
**Symptoms:**
```
⚠️ No agent output found for validation
```

**Solution:**
1. Ensure agent logs its output:
```bash
# Create expected output file
touch logs/story-6.2-agent-output.txt
```

2. Or run without comprehensive checks:
```bash
python tools/mvp.py story-6.2  # Basic validation only
```

### **Problem: YAML config errors**
**Symptoms:**
```
YAML parsing error in config/security.yaml
```

**Solution:**
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('config/security.yaml'))"

# Fix common issues:
# - Ensure proper indentation (2 spaces)
# - Check for missing colons
# - Validate quotes around strings
```

### **Problem: Budget alerts too sensitive**
**Symptoms:**
Daily budget alerts triggering too frequently

**Solution:**
```bash
# Edit config/cost-tracking.yaml
# Increase budget or adjust thresholds
```

## 🔍 Debugging Commands

### Check system setup
```bash
# Verify Python version
python --version  # Should be 3.7+

# Check required libraries
python -c "import yaml, json, datetime; print('All dependencies available')"

# Test basic functionality
python tools/mvp.py --help
```

### Validate configuration
```bash
# Test security config
python tools/security-analyzer.py scan-text "test prompt"

# Test cost tracking
python tools/cost-reporter.py report --days 1

# Test basic validation
python tools/mvp.py story-6.2
```

### Check file permissions
```bash
# Ensure logs directory is writable
ls -la logs/
chmod 755 logs/

# Check config file permissions
ls -la config/
chmod 644 config/*.yaml
```

## 📋 Environment Setup Checklist

### **First Time Setup**
```bash
# 1. Verify directory structure
tree -L 3  # Should show all expected directories

# 2. Check Python installation
python --version
pip install pyyaml  # If YAML errors occur

# 3. Test basic tools
python tools/mvp.py --help
python tools/security-analyzer.py --help
python tools/cost-reporter.py --help

# 4. Create required directories if missing
mkdir -p logs/ artifacts/validations/
```

### **Verification Steps**
```bash
# Run all tools to ensure they work
echo "Testing security analyzer..."
python tools/security-analyzer.py scan-text "Hello world"

echo "Testing cost reporter..."
python tools/cost-reporter.py report --days 1

echo "Testing basic validation..."
python tools/mvp.py --help

echo "All tools ready!"
```

## 🆘 Getting Help

### **When to Ask for Help**
1. **Security alerts you don't understand**
2. **Cost calculations that seem wrong**
3. **Validation failures you can't explain**
4. **Configuration errors that persist**

### **Information to Include**
When reporting issues, include:
```
- Your operating system (macOS/Linux/Windows)
- Python version
- Exact error message
- Command you ran
- Relevant config files (sanitized)
```

### **Quick Support Commands**
```bash
# Generate system report
python -c "
import sys, platform, yaml
print('System:', platform.system())
print('Python:', sys.version.split()[0])
print('YAML available:', hasattr(yaml, 'safe_load'))
"

# Test file access
python -c "
import os
for f in ['config/security.yaml', 'config/cost-tracking.yaml']:
    print(f, os.path.exists(f))
"
```

## 🎯 Quick Recovery Commands

### **Reset to working state**
```bash
# Reset all logs (back up first!)
mv logs/ logs_backup_$(date +%Y%m%d_%H%M%S)
mkdir -p logs/

# Reset config to defaults
cp config/security.yaml config/security.yaml.backup
cp config/cost-tracking.yaml config/cost-tracking.yaml.backup

# Re-run setup
python tools/mvp.py --help
```

### **Test everything works**
```bash
# Run comprehensive test
python tools/mvp.py test-story --comprehensive || echo "Test validation failed"
```

## 📚 Additional Resources

- [AI Security Guide](../user-guides/ai-security-guide.md)
- [Cost Management Guide](../user-guides/cost-management-guide.md)
- [README.md](../../README.md) - Main documentation