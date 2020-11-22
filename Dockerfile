# Multi-stage build:
FROM python:3.8-slim as ffmpegbase
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libffi-dev \
        libnacl-dev \
        python-dev && \
    rm -rf /var/lib/apt/lists* && \
    apt-get -y autoremove && \
    apt-get -y autoclean

FROM ffmpegbase as builder

# Suppress the annoying pip version check and disable caching to
# save space.
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1

# Copy everything in.
WORKDIR /disquip-bot
COPY . /disquip-bot

# Install requirements, run tests, and then install the package.
RUN pip install --no-cache-dir -r requirements.txt && \
    pytest tests --showlocals -v && \
    python setup.py sdist bdist_wheel

# The "runner" will be the final image.
FROM ffmpegbase as runner

# Suppress the annoying pip version check and disable caching to
# save space.
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1

# Copy in the installed wheel from the builder.
COPY --from=builder /disquip-bot/dist/*.whl /tmp/

# Install.
RUN pip install /tmp/*.whl && \
    rm -f /tmp/*.whl

WORKDIR /disquip-bot

# Run!
CMD ["disquip-bot"]
