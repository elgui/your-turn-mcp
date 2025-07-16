# Multi-stage build for minimal image size
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install runtime dependencies for audio support
RUN apt-get update && apt-get install -y \
    alsa-utils \
    pulseaudio-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user for security
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

# Set working directory
WORKDIR /app

# Copy application files
COPY mcp_your_turn_server.py .
COPY config.py .
COPY telegram_notifier.py .
COPY sound_manager.py .
COPY interactive_session.py .
COPY docker-entrypoint.sh .

# Make scripts executable
RUN chmod +x mcp_your_turn_server.py docker-entrypoint.sh

# Change ownership to non-root user
RUN chown -R mcpuser:mcpuser /app

# Switch to non-root user
USER mcpuser

# Set entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]

# Default command (can be overridden)
CMD []

# Metadata
LABEL maintainer="Enhanced MCP Your Turn Server"
LABEL description="Enhanced MCP server for LLM notifications and interactive communication via Telegram"
LABEL version="2.0.0"
