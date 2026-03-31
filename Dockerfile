# ================================
# Stage 1: Builder
# ================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install dependencies into a virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip --progress-bar off && \
    /opt/venv/bin/pip install --no-cache-dir --progress-bar off -r requirements.txt

# ================================
# Stage 2: Production
# ================================
FROM python:3.12-slim AS production

WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy only the app source code (not secrets, not local configs)
COPY . .

# Make sure we use the venv
ENV PATH="/opt/venv/bin:$PATH"

# Don't run as root
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Expose Flask port
EXPOSE 5000

# Run with gunicorn in production mode
# Replace "app:app" with your actual module:app_instance if different
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "1", "--timeout", "120", "run:app"]