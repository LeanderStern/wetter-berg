# ☃️ Wetter-Berg

A Discord bot that delivers daily snow forecast notifications for a configured mountain location. The bot fetches weather data from the [Open-Meteo API](https://open-meteo.com/) and posts snowfall reports to a designated Discord channel at a scheduled time each day.

## ✨ Features

- **Daily Snow Forecasts** — Automatically posts snowfall predictions to a Discord channel every day at a configurable hour.
- **Multi-Day Outlook** — Configurable forecast range (default: 4 days).
- **Detailed Reports** — Each forecast includes:
  - ❄️ Current snow depth
  - 🌨️ Expected new snowfall (cm)
  - 🔮 Precipitation probability (%)
  - 🕑 Hourly snowfall time intervals
- **Smart Notifications** — Only sends a message when snowfall is actually expected.
- **Caching** — API responses are cached for 1 hour to reduce unnecessary requests.
- **Retry Logic** — Automatic retries with exponential backoff for API calls.
- **Dockerized** — Easy deployment via Docker and Docker Compose with secure secret management.

## 📁 Project Structure

```
wetter-berg/
├── discord_client/
│   ├── __init__.py
│   └── discord_client.py       # Discord bot client with scheduled task
├── forecast_service/
│   ├── enums/
│   │   ├── __init__.py
│   │   ├── daily_weather_data_points_enum.py
│   │   └── hourly_weather_data_points_enum.py
│   ├── models/
│   │   ├── daily_snow_forecast_response.py
│   │   ├── hourly_snow_forecast_response.py
│   │   └── snowfall_hour_range.py
│   ├── __init__.py
│   └── forecast_service.py     # Open-Meteo API integration
├── secrets/
│   └── .gitkeep                # Place your discord_token.txt here
├── .dockerignore
├── .env                        # Environment configuration
├── .python-version
├── base_model.py               # Pydantic base model with logging
├── Dockerfile
├── docker-compose.yaml
├── entrypoint.sh               # Docker entrypoint for secret injection
├── main.py                     # Application entry point
├── pyproject.toml
└── uv.lock
```

## ⚙️ Configuration

All configuration is done through the `.env` file:

| Variable               | Description                                    | Example            |
| ---------------------- | ---------------------------------------------- | ------------------ |
| `BOT_TOKEN`            | Discord bot token (injected via Docker secret)  | `${DISCORD_TOKEN}` |
| `LOCAL`                | Locale for date formatting                     | `de_DE.UTF-8`      |
| `WEATHER_LATITUDE`     | Latitude of the location to monitor            | `51.18`            |
| `WEATHER_LONGITUDE`    | Longitude of the location to monitor           | `8.49`             |
| `TIMEZONE`             | Timezone for the forecast                      | `Europe/Berlin`    |
| `FORECAST_RANGE`       | Number of days to forecast                     | `4`                |
| `FORECAST_CHANNEL_ID`  | Discord channel ID for posting forecasts       | `1469816078...`    |
| `FORECAST_MESSAGE_HOUR`| Hour of the day (24h) to send the forecast     | `10`               |

## 🐳 Running with Docker

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed (included with Docker Desktop)
- A [Discord Bot Token](https://discord.com/developers/applications)

### Step 1: Clone the Repository

```bash
git clone https://github.com/LeanderStern/wetter-berg.git
cd wetter-berg
```

### Step 2: Configure Your Discord Bot Token

Create a file at `secrets/discord_token.txt` containing **only** your Discord bot token:

```bash
echo "YOUR_DISCORD_BOT_TOKEN" > secrets/discord_token.txt
```

> ⚠️ **Important:** Never commit this file to version control. The `secrets/` directory is already included in `.dockerignore`.

### Step 3: Configure the Environment

Edit the `.env` file to match your desired location and preferences:

```dotenv
BOT_TOKEN=${DISCORD_TOKEN}
LOCAL=de_DE.UTF-8
WEATHER_LATITUDE=51.18
WEATHER_LONGITUDE=8.49
TIMEZONE=Europe/Berlin
FORECAST_RANGE=4
FORECAST_CHANNEL_ID=YOUR_CHANNEL_ID
FORECAST_MESSAGE_HOUR=10
```

- Set `WEATHER_LATITUDE` and `WEATHER_LONGITUDE` to the coordinates of the mountain/location you want to track.
- Set `FORECAST_CHANNEL_ID` to the ID of the Discord channel where forecasts should be posted.
- Set `FORECAST_MESSAGE_HOUR` to the hour (24h format) when the bot should post the daily forecast.

### Step 4: Build and Run with Docker Compose

```bash
docker compose up -d --build
```

This will:
1. Build the Docker image based on `python:3.14-slim-trixie`
2. Install the `de_DE.UTF-8` locale for German date formatting (optional)
3. Install all dependencies using [uv](https://github.com/astral-sh/uv) (locked)
4. Inject your Discord token securely via Docker secrets
5. Start the bot in the background

### Viewing Logs

```bash
docker compose logs -f discord-bot
```

### Stopping the Bot

```bash
docker compose down
```

### Rebuilding After Changes

```bash
docker compose up -d --build
```

## 🔐 How Secrets Work

The project uses **Docker Compose secrets** to securely pass the Discord bot token to the container:

1. Your token is stored in `secrets/discord_token.txt` (not copied into the image thanks to `.dockerignore`)
2. Docker Compose mounts it at `/run/secrets/discord_token` inside the container
3. The `entrypoint.sh` script reads the secret and exports it as the `DISCORD_TOKEN` environment variable
4. The `.env` file references `${DISCORD_TOKEN}` to pass it to the bot as `BOT_TOKEN`

## 🛠️ Tech Stack

- **Python 3.14** (free-threaded)
- **[discord.py](https://discordpy.readthedocs.io/)** — Discord API wrapper
- **[Pydantic](https://docs.pydantic.dev/)** — Data validation and settings management
- **[Open-Meteo API](https://open-meteo.com/)** — Free weather forecast API (no API key required)
- **[uv](https://github.com/astral-sh/uv)** — Fast Python package manager
- **[Docker](https://www.docker.com/)** — Containerized deployment