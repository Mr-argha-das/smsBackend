from app.core.config import BaseAppSettings

class DevSettings(BaseAppSettings):
    debug: bool = True

settings = DevSettings()
