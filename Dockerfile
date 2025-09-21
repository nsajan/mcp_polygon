FROM python:3.13-slim

WORKDIR /app

# Copy only necessary files first for better caching
COPY pyproject.toml ./
COPY src/ ./src/
COPY entrypoint.py ./

# Install dependencies
RUN pip install --no-cache-dir -e .

# Make entrypoint executable
RUN chmod +x entrypoint.py

# Railway will set PORT environment variable for HTTP services
# For MCP server, we'll use the transport type from env
ENV MCP_TRANSPORT=${MCP_TRANSPORT:-stdio}

ENTRYPOINT ["python", "./entrypoint.py"]
