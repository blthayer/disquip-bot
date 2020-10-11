# Multi-stage build:
FROM blthayer/ffmpeg:buster as builder

# Suppress the annoying pip version check and disable caching to
# save space.
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=0

# Copy everything in.
WORKDIR /disquip-bot
COPY . /disquip-bot

# Install requirements, run tests, and then install the package. Since
# we're doing a multi-stage build, we'll run these in their own layers
# to help boost caching.
RUN pip install --no-cache-dir -r requirements.txt
RUN pytest tests --showlocals -v
RUN python setup.py sdist bdist_wheel

# Use a trim package to run locally.
FROM blthayer/ffmpeg:slim as runner

# Suppress the annoying pip version check and disable caching to
# save space.
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=0

# Copy in the installed wheel from the builder.
COPY --from=builder /disquip-bot/dist/*.whl /tmp/

# Install.
RUN pip install /tmp/*.whl && rm -f /tmp/*.whl

WORKDIR /disquip-bot

# Run!
CMD ["disquip-bot"]
