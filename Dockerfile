# The SFE's image: the factory at /factory, and the tools every run needs.
# Build it with tools/build-sfe.sh, which tags it with its factory version.
FROM debian:trixie-slim

# python3 runs the doc check script in the factory plugin. The factory's own Python, below,
# isn't on the PATH.
RUN apt-get update \
    && apt-get install --yes --no-install-recommends ca-certificates curl git make python3 \
    && curl --fail --silent --show-error --location \
        --output /usr/share/keyrings/githubcli-archive-keyring.gpg \
        https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg]" \
        "https://cli.github.com/packages stable main" \
        > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update \
    && apt-get install --yes --no-install-recommends gh \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.9.21 /uv /usr/local/bin/uv

# The factory's Python and virtual environment are outside /factory, so a checkout
# mounted at /factory leaves them in place. These settings are only for the build.
# The roles inherit the container's environment, so with them set there, `uv run` in a
# project would try to change the factory's own environment, which root owns.
ARG UV_PYTHON_INSTALL_DIR=/opt/sfe/python \
    UV_PROJECT_ENVIRONMENT=/opt/sfe/venv \
    UV_PYTHON_PREFERENCE=only-managed \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1
# Python doesn't write bytecode into /factory, which is read-only.
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /factory
# The packages first, so a change to the factory's own files reuses this layer.
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-install-project
COPY . .
# The factory is installed from /factory as it stands, so a mounted checkout's code is
# the code that runs.
RUN uv sync --locked

RUN useradd --create-home sfe
USER sfe
WORKDIR /home/sfe

ARG FACTORY_VERSION
ENV FACTORY_VERSION=$FACTORY_VERSION

ENTRYPOINT ["/opt/sfe/venv/bin/implementation-loop"]
