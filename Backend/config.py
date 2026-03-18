from os import getenv, path
import re
from dotenv import load_dotenv

CONFIG_ENV_PATH = path.join(path.dirname(path.dirname(__file__)), "config.env")

# Prefer runtime DATABASE (e.g. Heroku Config Vars); only rely on config.env
# for DATABASE when it is not set at runtime.
runtime_database = getenv("DATABASE")
if runtime_database is None:
    load_dotenv(CONFIG_ENV_PATH)
else:
    # Keep runtime env vars authoritative while still allowing missing local
    # values to be read from config.env.
    load_dotenv(CONFIG_ENV_PATH, override=False)


def _parse_csv_env(raw_value: str):
    return [item.strip() for item in (raw_value or "").split(",") if item.strip()]


def _mask_db_uri(uri: str) -> str:
    masked = re.sub(r"://(.*?):.*?@", r"://\1:*****@", uri)
    return masked.split("?")[0]


class Telegram:
    API_ID = int(getenv("API_ID", "0"))
    API_HASH = getenv("API_HASH", "")
    BOT_TOKEN = getenv("BOT_TOKEN", "")
    HELPER_BOT_TOKEN = getenv("HELPER_BOT_TOKEN", "")

    BASE_URL = getenv("BASE_URL", "").rstrip('/')
    PORT = int(getenv("PORT", "8000"))

    PARALLEL = int(getenv("PARALLEL", "1"))
    PRE_FETCH = int(getenv("PRE_FETCH", "1"))

    AUTH_CHANNEL = _parse_csv_env(getenv("AUTH_CHANNEL"))
    DATABASE = _parse_csv_env(getenv("DATABASE"))

    TMDB_API = getenv("TMDB_API", "")

    UPSTREAM_REPO = getenv("UPSTREAM_REPO", "")
    UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "")

    OWNER_ID = int(getenv("OWNER_ID", "5422223708"))

    REPLACE_MODE = getenv("REPLACE_MODE", "true").lower() == "true"
    HIDE_CATALOG = getenv("HIDE_CATALOG", "false").lower() == "true"
    # SKIP_MULTIPART = getenv("SKIP_MULTIPART", "true").lower() == "true"

    ADMIN_USERNAME = getenv("ADMIN_USERNAME", "fyvio")
    ADMIN_PASSWORD = getenv("ADMIN_PASSWORD", "fyvio")

    SUBSCRIPTION = getenv("SUBSCRIPTION", "false").lower() == "true"
    SUBSCRIPTION_GROUP_ID = int(getenv("SUBSCRIPTION_GROUP_ID", "0"))
    SUBSCRIPTION_URL = getenv("SUBSCRIPTION_URL", "https://t.me/")
    UPI_ID = getenv("UPI_ID", "")
    APPROVER_IDS = [int(x.strip()) for x in (getenv("APPROVER_IDS") or "").split(",") if x.strip().isdigit()]


print(f"[CONFIG] DATABASE URIs loaded: {len(Telegram.DATABASE)}")
if Telegram.DATABASE:
    print(f"[CONFIG] DATABASE URIs (masked): {[ _mask_db_uri(uri) for uri in Telegram.DATABASE ]}")
