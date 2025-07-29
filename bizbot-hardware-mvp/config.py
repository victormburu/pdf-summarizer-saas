import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional
import warnings

# Load environment variables from .env file
load_dotenv()

class DBConfig:
    """Secure database configuration with environment variables"""
    
    @staticmethod
    def get_config() -> Dict[str, Any]:
        """
        Get database configuration with type-safe defaults
        Returns:
            Dict[str, Any]: Database configuration dictionary
        Raises:
            ValueError: If required config is missing or invalid
        """
        config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": DBConfig._parse_int(os.getenv("DB_PORT")),  # Default handled in _parse_int
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),  # Most sensitive - no default!
            "database": os.getenv("DB_NAME"),
            "pool_name": "bizbot_pool",
            "pool_size": DBConfig._parse_int(os.getenv("DB_POOL_SIZE"), default=5, min_value=1, max_value=20),
            "autocommit": False,
            "ssl": DBConfig._parse_bool(os.getenv("DB_SSL"), default=False),
            "connect_timeout": 30,
            "charset": "utf8mb4",
            "collation": "utf8mb4_unicode_ci"
        }
        
        DBConfig._validate_config(config)
        DBConfig._warn_about_insecure_settings(config)
        return config

    @staticmethod
    def _parse_int(value: Optional[str], default: int = 3306, 
                  min_value: Optional[int] = None, 
                  max_value: Optional[int] = None) -> int:
        """Safely parse integer with constraints"""
        try:
            num = int(value) if value is not None else default
            if min_value is not None and num < min_value:
                warnings.warn(f"Value {num} is below minimum {min_value}, using {min_value}")
                return min_value
            if max_value is not None and num > max_value:
                warnings.warn(f"Value {num} exceeds maximum {max_value}, using {max_value}")
                return max_value
            return num
        except ValueError:
            warnings.warn(f"Invalid integer value '{value}', using default {default}")
            return default

    @staticmethod
    def _parse_bool(value: Optional[str], default: bool = False) -> bool:
        """Safely parse boolean from string"""
        if value is None:
            return default
        return value.lower() in ("true", "1", "t", "y", "yes")

    @staticmethod
    def _validate_config(config: Dict[str, Any]) -> None:
        """Validate critical database configuration"""
        if not config["password"]:
            raise ValueError("Database password must be set in environment variables")
        
        if not all(config[key] for key in ["host", "user", "database"]):
            raise ValueError("Missing required database configuration (host, user, or database)")
            
        if config["host"] in ("localhost", "127.0.0.1") and config["ssl"]:
            warnings.warn("SSL enabled for localhost connection - this is unnecessary")

    @staticmethod
    def _warn_about_insecure_settings(config: Dict[str, Any]) -> None:
        """Warn about potentially insecure settings"""
        if config["password"] == "NewSecurePassword123!":
            warnings.warn("Default password detected - change this in production!", RuntimeWarning)
            
        if not config["ssl"] and config["host"] not in ("localhost", "127.0.0.1"):
            warnings.warn("SSL is disabled for remote connection - this is insecure!", RuntimeWarning)
            
        if config["user"] == "root":
            warnings.warn("Using root database user is not recommended", RuntimeWarning)

# Example usage with error handling
try:
    db_config = DBConfig.get_config()
    print("Database configuration loaded successfully")
    # Connect to database using these settings...
except ValueError as e:
    print(f"Configuration error: {e}")
    # Handle error (exit, use defaults, etc.)
except Exception as e:
    print(f"Unexpected error: {e}")