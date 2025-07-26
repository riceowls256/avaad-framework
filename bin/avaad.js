#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const PACKAGE_ROOT = path.dirname(__dirname);
const TOOLS_DIR = path.join(PACKAGE_ROOT, 'tools');

function runPythonScript(scriptName, args = []) {
  const scriptPath = path.join(TOOLS_DIR, scriptName);
  
  if (!fs.existsSync(scriptPath)) {
    console.error(`❌ Script not found: ${scriptPath}`);
    process.exit(1);
  }

  const pythonArgs = [scriptPath, ...args];
  const pythonProcess = spawn('python3', pythonArgs, {
    stdio: 'inherit',
    cwd: PACKAGE_ROOT
  });

  pythonProcess.on('error', (error) => {
    if (error.code === 'ENOENT') {
      console.error('❌ Python3 not found. Please install Python 3.7 or higher.');
    } else {
      console.error('❌ Error running Python:', error.message);
    }
    process.exit(1);
  });

  pythonProcess.on('close', (code) => {
    process.exit(code);
  });
}

function main() {
  const [,, command, ...args] = process.argv;

  if (!command) {
    console.log(`
🎯 AVAAD Framework - Automated Verification for AI-Assisted Development

Usage:
  avaad <story-id> [--comprehensive]    Validate a story
  avaad security <args...>             Run security analyzer
  avaad cost <args...>                 Run cost reporter
  avaad update                         Update framework from GitHub
  avaad version                        Show version info

Examples:
  avaad 6.2
  avaad 6.2 --comprehensive
  avaad security scan-story --story 6.2
  avaad cost report --last-week
    `);
    return;
  }

  switch (command) {
    case 'security':
      runPythonScript('security-analyzer.py', args);
      break;
    
    case 'cost':
      runPythonScript('cost-reporter.py', args);
      break;
    
    case 'update':
      updateFramework();
      break;
    
    case 'version':
      showVersion();
      break;
    
    default:
      // Assume it's a story ID for validation
      const storyArgs = [command];
      if (args.includes('--comprehensive')) {
        storyArgs.push('--comprehensive');
      }
      runPythonScript('mvp.py', storyArgs);
  }
}

function updateFramework() {
  console.log('🔄 Updating AVAAD framework from GitHub...');
  
  const npmUpdate = spawn('npm', ['update', 'avaad-framework'], {
    stdio: 'inherit',
    cwd: process.cwd()
  });

  npmUpdate.on('close', (code) => {
    if (code === 0) {
      console.log('✅ AVAAD framework updated successfully!');
    } else {
      console.error('❌ Update failed. Check your internet connection.');
    }
    process.exit(code);
  });
}

function showVersion() {
  const packageJson = require('../package.json');
  console.log(`AVAAD Framework v${packageJson.version}`);
  console.log(`Repository: ${packageJson.repository.url}`);
}

if (require.main === module) {
  main();
}