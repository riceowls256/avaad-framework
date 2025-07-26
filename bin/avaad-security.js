#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const PACKAGE_ROOT = path.dirname(__dirname);
const TOOLS_DIR = path.join(PACKAGE_ROOT, 'tools');

function main() {
  const args = process.argv.slice(2);
  const scriptPath = path.join(TOOLS_DIR, 'security-analyzer.py');
  
  const pythonProcess = spawn('python3', [scriptPath, ...args], {
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

if (require.main === module) {
  main();
}