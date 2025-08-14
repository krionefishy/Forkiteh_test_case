from pathlib import Path 
import yaml
import os

class Settings:
    DATABASE_URL: str = None
    LOGGING_LEVEL: str = "DEBUG"
    TRON_NETWORK: str = "mainnet"


def setup_config(config_path: str = "config.yaml") -> Settings:
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    database = data.get("database")

    if not database:
        raise ValueError("Missing 'database' params")
    host = database["host"]
    port = database["port"]
    user = database["user"]
    password = database["password"]
    db_name = database["database"]

    Settings.DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"

    Settings.LOGGING_LEVEL = data.get("logging", {}).get("level", "INFO")
    if Settings.LOGGING_LEVEL not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
        Settings.LOGGING_LEVEL = "INFO"

    Settings.TRON_NETWORK = data.get("tron", {}).get("network", "mainnet")
    if Settings.TRON_NETWORK not in ("mainnet", "shasta", "nile"):
        Settings.TRON_NETWORK = "mainnet"

    return Settings
        