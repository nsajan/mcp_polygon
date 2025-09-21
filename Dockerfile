FROM python:3.13-slim

WORKDIR /app

# Install uv for faster, more reliable dependency management
RUN pip install uv

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Create a minimal README to satisfy build requirements
RUN echo "# MCP Polygon Server" > README.md

# Install dependencies using uv with locked versions
RUN uv pip install --system --no-cache .

# Copy application code
COPY src/ ./src/
COPY entrypoint.py ./

# Make entrypoint executable
RUN chmod +x entrypoint.py

# Railway will set PORT environment variable for HTTP services
# For MCP server, we'll use the transport type from env
ENV MCP_TRANSPORT=${MCP_TRANSPORT:-stdio}

ENTRYPOINT ["python", "./entrypoint.py"]
