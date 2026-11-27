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

# Node and Python for the projects to use (TD-13). Debian's nodejs package isn't Node 24.
ARG NODE_VERSION=24.21.0
RUN case "$(dpkg --print-architecture)" in \
        amd64) arch=x64 sha256=6e1db87ef58b8819e5d5402eff1536491b18edd8eb7bee5ef7897876e88dc5ff ;; \
        arm64) arch=arm64 sha256=724282c3b43aec998aa9527380465b45d229e021b58035f5f4f63095eabfe5d5 ;; \
        *) echo "No Node build for $(dpkg --print-architecture)" >&2; exit 1 ;; \
    esac \
    && tarball="node-v$NODE_VERSION-linux-$arch.tar.gz" \
    && curl --fail --silent --show-error --location --output "/tmp/$tarball" \
        "https://nodejs.org/dist/v$NODE_VERSION/$tarball" \
    && echo "$sha256  /tmp/$tarball" | sha256sum --check --strict \
    && tar --extract --gzip --file "/tmp/$tarball" --directory /usr/local --strip-components 1 \
        --exclude CHANGELOG.md --exclude LICENSE --exclude README.md \
    && rm "/tmp/$tarball"
# uv links python3.14 into /usr/local/bin, where a project's `uv sync` finds it on the PATH, so
# it downloads no Python. This runs before the factory's uv settings below, so the projects'
# Python stays apart from the factory's.
RUN UV_PYTHON_INSTALL_DIR=/opt/python UV_PYTHON_BIN_DIR=/usr/local/bin UV_NO_CACHE=1 \
    uv python install 3.14.2

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

# The user ID of whoever builds the image, which tools/build-sfe.sh passes in. So the files the SFE
# writes in the run folder, which run-sfe.sh mounts, belong to that user outside the SFE. run-sfe.sh
# reads the label to check it.
ARG SFE_UID=1000
LABEL software-factory.sfe-uid=$SFE_UID
RUN useradd --create-home --uid "$SFE_UID" sfe
USER sfe
WORKDIR /home/sfe
# Where run-sfe.sh mounts the run folder. Docker would make each missing folder on the way as root,
# and then Claude Code couldn't write its other files in ~/.claude.
RUN mkdir --parents /home/sfe/run /home/sfe/.claude/projects

ARG FACTORY_VERSION
ENV FACTORY_VERSION=$FACTORY_VERSION

ENTRYPOINT ["/opt/sfe/venv/bin/implementation-loop"]
