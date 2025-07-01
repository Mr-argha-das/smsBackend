from app.core.config import BaseAppSettings

class ProdSettings(BaseAppSettings):
    debug: bool = False

settings = ProdSettings()
