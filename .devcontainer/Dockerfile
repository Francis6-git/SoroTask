FROM mcr.microsoft.com/devcontainers/rust:1-1-bullseye

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Install additional tools
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libssl-dev \
    protobuf-compiler \
    git \
    curl \
    wget \
    jq \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Rust wasm target for Soroban contracts
RUN rustup target add wasm32-unknown-unknown

# Install npm global tools
RUN npm install -g \
    yarn \
    pnpm \
    @stellar/soroban-cli

# Create non-root user for development
USER vscode

# Set working directory
WORKDIR /workspace
