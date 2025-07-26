#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const PROJECT_ROOT = process.cwd();
const AVAAD_DIR = path.join(PROJECT_ROOT, '.avaad');

console.log('🔄 Updating AVAAD Framework...');

const npmUpdate = spawn('npm', ['update', 'avaad-framework'], {
  stdio: 'inherit',
  cwd: AVAAD_DIR
});

npmUpdate.on('close', (code) => {
  if (code === 0) {
    console.log('✅ AVAAD framework updated successfully!');
    console.log('');
    console.log('🚀 Updated tools available:');
    console.log('  npx avaad story-id');
    console.log('  npx avaad cost report --last-week');
    console.log('  npx avaad security report --last-day');
  } else {
    console.error('❌ Update failed');
  }
});