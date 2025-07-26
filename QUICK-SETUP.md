# NPM Package Setup - Cross-Project Synchronization

## 🚀 Quick Setup for Other Projects

### **1. Install AVAAD in Your Other Project**
```bash
# In your other project directory (e.g., fin_data_ingestor)
cd /path/to/your/other/project

# Install from npm
npm install avaad-framework

# OR install directly from GitHub
npm install riceowls256/avaad-framework
```

### **2. Use Installed Tools**
```bash
# Validate stories
npx avaad 6.2
npx avaad 6.2 --comprehensive

# Security analysis
npx avaad-security scan-story --story 6.2
npx avaad-security report --last-week

# Cost management
npx avaad-cost budget --daily
npx avaad-cost report --last-week
```

### **3. Update Framework**
```bash
# Update to latest version
npm update avaad-framework

# Check current version
npx avaad version
```

## 📁 Automatic Project Integration

### **Option 1: NPM Package (Recommended)**
Add to your other project's `package.json`:
```json
{
  "devDependencies": {
    "avaad-framework": "latest"
  },
  "scripts": {
    "validate": "npx avaad",
    "security": "npx avaad-security",
    "cost": "npx avaad-cost"
  }
}
```

Then run:
```bash
npm install
npm run validate 6.2
npm run security scan-story --story 6.2
```

### **Option 2: Git Submodule (Alternative)**
```bash
# In your other project
git submodule add https://github.com/riceowls256/avaad-framework.git .avaad
git submodule update --init --recursive

# Use directly
./.avaad/tools/mvp.py 6.2
```

### **Option 3: Manual Git Clone**
```bash
# In your other project
git clone https://github.com/riceowls256/avaad-framework.git .avaad

# Add to .gitignore
echo ".avaad/" >> .gitignore

# Use tools
./.avaad/tools/mvp.py 6.2
```

## 🔄 Automatic Updates

### **NPM Updates**
```bash
# Regular updates
npm update avaad-framework

# Check for updates
npm outdated avaad-framework

# Update to specific version
npm install avaad-framework@2.1.1
```

### **GitHub Updates**
```bash
# Update from GitHub directly
npm install riceowls256/avaad-framework#main
```

## 🎯 Usage Examples in Other Projects

### **Daily Workflow**
```bash
# In your fin_data_ingestor project
npx avaad cost budget --daily          # Check daily budget
npx avaad 6.2 --comprehensive          # Validate story with security & cost
npx avaad-security report --last-week  # Security summary
```

### **Package.json Integration**
```json
{
  "scripts": {
    "validate-story": "npx avaad",
    "security-check": "npx avaad-security",
    "cost-report": "npx avaad-cost",
    "update-avaad": "npm update avaad-framework"
  }
}
```

### **VS Code Integration**
Add to `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "AVAAD: Validate Story",
      "type": "shell",
      "command": "npx avaad ${input:storyId}"
    },
    {
      "label": "AVAAD: Security Check",
      "type": "shell", 
      "command": "npx avaad-security scan-story --story ${input:storyId}"
    }
  ]
}
```

## 🛠️ Troubleshooting Cross-Project Issues

### **Python Path Issues**
```bash
# If Python not found, set path
export PYTHONPATH="/usr/local/bin/python3:$PYTHONPATH"
npx avaad 6.2
```

### **Permission Issues**
```bash
# Fix permissions
chmod +x node_modules/avaad-framework/bin/*.js
chmod +x node_modules/avaad-framework/tools/*.py
```

### **Node Version Issues**
```bash
# Ensure Node 14+
node --version  # Should be 14.0.0+
```

## 📊 Project Structure with AVAAD

```
your-project/
├── .avaad/                    # AVAAD framework (if using git clone)
├── node_modules/
│   └── avaad-framework/       # NPM package
├── package.json               # Your project package.json
├── logs/                      # AVAAD logs (auto-created)
├── config/                    # AVAAD config (auto-created)
└── ...
```

## 🚀 Quick Commands Summary

| Task | NPM Command | Direct Command |
|------|-------------|----------------|
| Validate story | `npx avaad 6.2` | `python tools/mvp.py 6.2` |
| Security scan | `npx avaad-security scan-story --story 6.2` | `python tools/security-analyzer.py scan-story --story 6.2` |
| Cost report | `npx avaad-cost report --last-week` | `python tools/cost-reporter.py report --last-week` |
| Update framework | `npm update avaad-framework` | `git pull` |

## ✅ Verification Steps

1. **Test installation:**
   ```bash
   npx avaad version
   ```

2. **Test basic functionality:**
   ```bash
   npx avaad --help
   ```

3. **Test cost tracking:**
   ```bash
   npx avaad-cost budget --daily
   ```

4. **Test security:**
   ```bash
   npx avaad-security scan-text "test prompt"
   ```

## 🔄 Sync Strategy

- **NPM Package**: Automatic updates via `npm update`
- **GitHub**: Direct updates from main branch
- **Local**: Manual updates when needed

The NPM package approach ensures your other projects always have the latest AVAAD features with a simple `npm update` command!