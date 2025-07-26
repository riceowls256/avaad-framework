#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const PROJECT_ROOT = process.cwd();
const AVAAD_DIR = path.join(PROJECT_ROOT, '.avaad');

console.log('🎯 Installing AVAAD Framework...');

// Create .avaad directory if it doesn't exist
if (!fs.existsSync(AVAAD_DIR)) {
  fs.mkdirSync(AVAAD_DIR, { recursive: true });
  console.log('✅ Created .avaad directory');
}

// Create package.json in .avaad if it doesn't exist
const packagePath = path.join(AVAAD_DIR, 'package.json');
if (!fs.existsSync(packagePath)) {
  const packageJson = {
    "name": "avaad-local",
    "version": "1.0.0",
    "description": "Local AVAAD framework installation",
    "dependencies": {
      "avaad-framework": "latest"
    }
  };
  fs.writeFileSync(packagePath, JSON.stringify(packageJson, null, 2));
  console.log('✅ Created local package.json');
}

// Install dependencies
console.log('📦 Installing AVAAD dependencies...');
const npmInstall = spawn('npm', ['install'], {
  stdio: 'inherit',
  cwd: AVAAD_DIR
});

npmInstall.on('close', (code) => {
  if (code === 0) {
    console.log('✅ AVAAD framework installed successfully!');
    console.log('');
    console.log('🚀 Next steps:');
    console.log('  cd .avaad');
    console.log('  npx avaad story-id');
    console.log('  npx avaad cost budget --daily');
    console.log('  npx avaad security scan-story --story 6.2');
  } else {
    console.error('❌ Installation failed');
  }
});