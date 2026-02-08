#!/bin/bash
set -e

export DISCORD_TOKEN=$(cat /run/secrets/discord_token)

exec "$@"