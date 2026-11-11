# ─── Building ───
FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir uv \
&& uv venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv \
PATH=/opt/venv/bin:$PATH
RUN uv pip install --no-cache .
# Copy src & dependencies into builds, setup environment (+packages) and run
# ─── Runtime ───
FROM python:3.12-slim
WORKDIR /app
RUN groupadd -r app && \
useradd -r -g app -d /app app && \
chown app:app /app
# Copy environment from build
COPY --from=builder --chown=app:app /opt/venv /opt/venv
# Source nằm trong package đã cài
ENV VIRTUAL_ENV=/opt/venv \ 
    PATH="/opt/venv/bin:$PATH" \ 
    PYTHONUNBUFFERED=1
USER app
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "product_api.factory:create_app()"]