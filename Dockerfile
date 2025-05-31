##############################
# Poetry install build stage #
##############################

# Make sure Python version is in sync with CI configs
FROM python:3.13-slim-bookworm AS poetry-install

# Install Poetry
# Make sure Poetry version is in sync with CI configs
ENV POETRY_VERSION=2.1.3
ENV POETRY_HOME=/opt/poetry
ENV PATH=/opt/poetry/bin:$PATH
ADD https://install.python-poetry.org /tmp/poetry-install.py
RUN python3 /tmp/poetry-install.py

####################
# Base build stage #
####################

# Make sure Python version is in sync with CI configs
FROM python:3.13-slim-bookworm AS base

# Configure apt to keep downloaded packages for BuildKit caching
# https://docs.docker.com/reference/dockerfile/#example-cache-apt-packages
RUN rm -f /etc/apt/apt.conf.d/docker-clean \
  && echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

# Set up unprivileged user
RUN useradd --create-home kalokohan

# Set up project directory
ENV APP_DIR=/app
RUN mkdir -p "$APP_DIR" \
  && chown -R kalokohan:kalokohan "$APP_DIR"

# Set up node_modules so it's owned and writable by the unprivileged user
RUN mkdir -p "$APP_DIR/node_modules" \
  && chown -R kalokohan:kalokohan "$APP_DIR/node_modules"

# Set up virtualenv
ENV VIRTUAL_ENV=/venv
ENV PATH=/venv/bin:$PATH
RUN mkdir -p /venv \
  && python3 -m venv /venv \
  && chown -R kalokohan:kalokohan /venv

# Switch to unprivileged user
USER kalokohan

# Switch to project directory
WORKDIR $APP_DIR

# Set environment variables
# - PYTHONUNBUFFERED: Force Python stdout and stderr streams to be unbuffered
# - PORT: Set port that is used by Gunicorn. This should match the "EXPOSE"
#   command
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Port used by this container to serve HTTP
EXPOSE 8000

# Serve project with gunicorn
CMD ["gunicorn", "kalokohan.wsgi:application"]

##############################
# Pre-production build stage #
##############################

FROM base AS pre-production

# Switch to root to install packages from apt
USER root

# Download NodeSource apt setup script
ADD https://deb.nodesource.com/setup_22.x /tmp/nodesource-setup.sh

# Install Node.js for Node dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  bash /tmp/nodesource-setup.sh \
  # The NodeSource setup script already runs apt-get update
  && apt-get install -y nodejs

# Switch back to unprivileged user
USER kalokohan

# Copy Poetry from poetry-install
ENV POETRY_HOME=/opt/poetry
ENV PATH=/opt/poetry/bin:$PATH
COPY --from=poetry-install --chown=kalokohan:kalokohan /opt/poetry /opt/poetry

# Install main project dependencies
RUN --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml \
  --mount=type=bind,source=poetry.lock,target=/app/poetry.lock \
  --mount=type=cache,target=/home/kalokohan/.cache/pypoetry,uid=1000 \
  --mount=type=cache,target=/home/kalokohan/.cache/pip,uid=1000 \
  poetry install --only main

# Install Node dependencies
RUN --mount=type=bind,source=package.json,target=/app/package.json \
  --mount=type=bind,source=package-lock.json,target=/app/package-lock.json \
  --mount=type=cache,target=/home/kalokohan/.npm,uid=1000 \
  npm ci

# Copy the project files
# Ensure that this is one of the last commands for better layer caching
COPY --chown=kalokohan:kalokohan . .

# Build minified Tailwind styles
RUN npx tailwindcss -i kalokohan/static_src/tailwind/styles.css -o kalokohan/static_built/tailwind/styles.css --minify

# Collect staticfiles
RUN SECRET_KEY=dummy python3 manage.py collectstatic --noinput --clear

##########################
# Production build stage #
##########################

FROM base AS production

# Temporarily switch to install packages from apt
USER root

# Install libpq-dev for psycopg
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update \
  && apt-get install -y libpq-dev

# Switch back to unprivileged user
USER kalokohan

# Copy Poetry from poetry-install
ENV POETRY_HOME=/opt/poetry
ENV PATH=/opt/poetry/bin:$PATH
COPY --from=poetry-install --chown=kalokohan:kalokohan /opt/poetry /opt/poetry

# Copy virtualenv from pre-production
COPY --from=pre-production --chown=kalokohan:kalokohan /venv /venv

# Copy staticfiles from pre-production
COPY --from=pre-production --chown=kalokohan:kalokohan /app/static_collected /app/static_collected

# Copy the project files
# Ensure that this is one of the last commands for better layer caching
COPY --chown=kalokohan:kalokohan . .

###################
# Dev build stage #
###################

FROM base AS dev

# Temporarily switch to install packages from apt
USER root

# Download Postgres PGP public key
ADD https://www.postgresql.org/media/keys/ACCC4CF8.asc /tmp/postgresql-pgp-public-key.asc

# Download NodeSource apt setup script
ADD https://deb.nodesource.com/setup_22.x /tmp/nodesource-setup.sh

# Install gnupg for installing Postgres client
# Install git for pre-commit
# Install Node.js for Node dependencies
# Install Postgres client for dslr import and export
# Install gettext for i18n
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update \
  && apt-get install -y gnupg \
  && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
  && cat /tmp/postgresql-pgp-public-key.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg >/dev/null \
  && bash /tmp/nodesource-setup.sh \
  # The NodeSource setup script already runs apt-get update
  && apt-get install -y git nodejs postgresql-client-16 gettext

# Switch back to unprivileged user
USER kalokohan

# Copy Poetry from poetry-install
ENV POETRY_HOME=/opt/poetry
ENV PATH=/opt/poetry/bin:$PATH
COPY --from=poetry-install --chown=kalokohan:kalokohan /opt/poetry /opt/poetry

# Install Node dependencies
RUN --mount=type=bind,source=package.json,target=/app/package.json \
  --mount=type=bind,source=package-lock.json,target=/app/package-lock.json \
  --mount=type=cache,target=/home/kalokohan/.npm,uid=1000 \
  npm ci

# Install all project dependencies
RUN --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml \
  --mount=type=bind,source=poetry.lock,target=/app/poetry.lock \
  --mount=type=cache,target=/home/kalokohan/.cache/pypoetry,uid=1000 \
  --mount=type=cache,target=/home/kalokohan/.cache/pip,uid=1000 \
  poetry install

# Add bash aliases
RUN echo "alias dj='python3 manage.py'" >> $HOME/.bash_aliases
RUN echo "alias djrun='python3 manage.py runserver 0:8000'" >> $HOME/.bash_aliases
RUN echo "alias djtest='python3 manage.py test --settings=kalokohan.settings.test -v=2'" >> $HOME/.bash_aliases
RUN echo "alias djtestkeepdb='python3 manage.py test --settings=kalokohan.settings.test -v=2 --keepdb'" >> $HOME/.bash_aliases
RUN echo "alias twwatch='npm run tailwind:watch'" >> $HOME/.bash_aliases

# Copy the project files
# Ensure that this is one of the last commands for better layer caching
COPY --chown=kalokohan:kalokohan . .
