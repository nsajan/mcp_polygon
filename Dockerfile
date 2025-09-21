FROM python:3.13-slim

WORKDIR /app

# Install dependencies directly with pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY entrypoint.py ./

# Make entrypoint executable
RUN chmod +x entrypoint.py

# Railway will set PORT environment variable for HTTP services
# For MCP server, we'll use the transport type from env
ENV MCP_TRANSPORT=${MCP_TRANSPORT:-stdio}

ENTRYPOINT ["python", "./entrypoint.py"]
