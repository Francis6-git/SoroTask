#!/bin/bash
set -e

echo "Installing dependencies..."

# Update package lists
apt-get update

# Install Node.js dependencies globally
npm install -g yarn pnpm

# Install Python (required for some build tools)
apt-get install -y python3 python3-pip

# Install Stellar CLI
curl https://github.com/stellar/js-stellar-sdk/releases/latest -L -o stellar-cli.tar.gz 2>/dev/null || true

# Add Soroban CLI
npm install -g @stellar/soroban-cli || true

echo "Installing project dependencies..."

# Install dependencies for each workspace
if [ -f "contract/Cargo.toml" ]; then
  echo "Building Rust contract..."
  cd contract
  cargo build --target wasm32-unknown-unknown --release
  cd ..
fi

if [ -f "keeper/package.json" ]; then
  echo "Installing keeper dependencies..."
  cd keeper
  npm install
  cd ..
fi

if [ -f "frontend/package.json" ]; then
  echo "Installing frontend dependencies..."
  cd frontend
  npm install
  cd ..
fi

echo "Development environment setup completed!"
