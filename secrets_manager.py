#!/usr/bin/env python3
"""
INTELLIGENT SECRETS MANAGER
Handles all API keys, tokens, passwords, and secrets securely
Never asks twice - stores once and uses everywhere
Works like a real team member - smart and autonomous
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict
from dotenv import load_dotenv, set_key

PROJECT_ROOT = Path(__file__).parent
ENV_FILE = PROJECT_ROOT / ".env"
ENV_EXAMPLE_FILE = PROJECT_ROOT / ".env.example"


class SecretsManager:
    """
    Intelligent secrets manager that:
    - Stores secrets securely in .env
    - Never asks for the same secret twice
    - Provides secrets to all agents automatically
    - Works like a real team member (smart, autonomous)
    """

    def __init__(self):
        # Load existing .env file
        load_dotenv(ENV_FILE)
        self.secrets = {}
        self._load_secrets()

    def _load_secrets(self):
        """Load all secrets from environment"""
        self.secrets = {
            # Anthropic/Claude
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),

            # Amazon
            "AMAZON_SELLER_ID": os.getenv("AMAZON_SELLER_ID"),
            "AMAZON_MWS_KEY": os.getenv("AMAZON_MWS_KEY"),
            "AMAZON_MWS_SECRET": os.getenv("AMAZON_MWS_SECRET"),

            # Stripe
            "STRIPE_SECRET_KEY": os.getenv("STRIPE_SECRET_KEY"),
            "STRIPE_PUBLISHABLE_KEY": os.getenv("STRIPE_PUBLISHABLE_KEY"),

            # Database
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),

            # Redis
            "REDIS_URL": os.getenv("REDIS_URL"),

            # Clerk
            "CLERK_SECRET_KEY": os.getenv("CLERK_SECRET_KEY"),

            # External APIs
            "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),

            # Email
            "RESEND_API_KEY": os.getenv("RESEND_API_KEY"),

            # Business
            "BUSINESS_EMAIL": os.getenv("BUSINESS_EMAIL"),
            "OWNER_EMAIL": os.getenv("OWNER_EMAIL"),
        }

    def get(self, key: str, secret_type: str = "api_key") -> Optional[str]:
        """
        Get a secret intelligently:
        1. Check if already stored in .env
        2. If not, ask user once and store it
        3. Return the secret

        Never asks twice - stores and reuses
        """
        # Check if already set
        if key in self.secrets and self.secrets[key]:
            return self.secrets[key]

        # If not set, ask user (only once)
        secret_value = self._ask_for_secret(key, secret_type)

        if secret_value:
            # Store it for future use
            self._store_secret(key, secret_value)
            self.secrets[key] = secret_value
            return secret_value

        return None

    def _ask_for_secret(self, key: str, secret_type: str) -> Optional[str]:
        """Ask user for a secret (friendly way, like a real team member)"""

        # Human-friendly prompts
        friendly_names = {
            "ANTHROPIC_API_KEY": "Claude API Key",
            "AMAZON_SELLER_ID": "Amazon Seller ID",
            "STRIPE_SECRET_KEY": "Stripe Secret Key",
            "DATABASE_URL": "Database URL",
            "RESEND_API_KEY": "Resend Email API Key",
            "GOOGLE_API_KEY": "Google API Key",
            "OPENAI_API_KEY": "OpenAI API Key",
        }

        friendly_name = friendly_names.get(key, key)

        print(f"\n{'='*60}")
        print(f"[SECRETS MANAGER] Need: {friendly_name}")
        print(f"{'='*60}")
        print(f"Type: {secret_type}")
        print(f"This will be stored in .env (kept secret, never committed)")
        print(f"You'll only need to provide this once\n")

        value = input(f"Enter {friendly_name}: ").strip()

        if value:
            print(f"✓ {friendly_name} stored securely in .env\n")
            return value
        else:
            print(f"✗ Skipped {friendly_name} - can be added later\n")
            return None

    def _store_secret(self, key: str, value: str):
        """Store secret in .env file"""
        try:
            # Create .env if it doesn't exist
            if not ENV_FILE.exists():
                ENV_FILE.write_text("")

            # Add or update the secret
            set_key(str(ENV_FILE), key, value)
        except Exception as e:
            print(f"Warning: Could not store {key} in .env: {str(e)}")

    def has_secret(self, key: str) -> bool:
        """Check if a secret is configured"""
        return key in self.secrets and self.secrets[key] is not None

    def require_secret(self, key: str, secret_type: str = "api_key") -> str:
        """Get secret and fail if not available"""
        secret = self.get(key, secret_type)
        if not secret:
            raise ValueError(f"Required secret {key} not configured")
        return secret

    def get_all_secrets(self) -> Dict[str, Optional[str]]:
        """Get all configured secrets (for debugging)"""
        return {k: v for k, v in self.secrets.items() if v is not None}

    def print_status(self):
        """Print which secrets are configured"""
        print(f"\n{'='*60}")
        print("SECRETS CONFIGURED")
        print(f"{'='*60}\n")

        configured = {k: v for k, v in self.secrets.items() if v}
        unconfigured = {k: v for k, v in self.secrets.items() if not v}

        if configured:
            print("✓ CONFIGURED:")
            for key in configured.keys():
                print(f"  • {key}")

        if unconfigured:
            print(f"\n✗ NOT CONFIGURED ({len(unconfigured)}):")
            for key in unconfigured.keys():
                print(f"  • {key}")

        print(f"\n{'='*60}\n")

    @staticmethod
    def create_env_from_user():
        """Interactive setup - ask user to configure all secrets"""
        print(f"\n{'='*60}")
        print("INTERACTIVE SECRETS SETUP")
        print("Configure your secrets once, use everywhere")
        print(f"{'='*60}\n")

        manager = SecretsManager()

        # Essential secrets
        essential_keys = [
            ("ANTHROPIC_API_KEY", "api_key"),
            ("AMAZON_SELLER_ID", "amazon_id"),
            ("STRIPE_SECRET_KEY", "stripe_key"),
        ]

        print("ESSENTIAL SECRETS (required for basic operation):\n")
        for key, secret_type in essential_keys:
            if not manager.has_secret(key):
                manager.get(key, secret_type)

        print("\nOPTIONAL SECRETS (add later if needed):\n")
        optional_keys = [
            ("GOOGLE_API_KEY", "api_key"),
            ("OPENAI_API_KEY", "api_key"),
            ("RESEND_API_KEY", "api_key"),
        ]

        for key, secret_type in optional_keys:
            if not manager.has_secret(key):
                response = input(f"Configure {key}? (y/n): ").strip().lower()
                if response == 'y':
                    manager.get(key, secret_type)

        manager.print_status()
        return manager


# Global instance
_manager: Optional[SecretsManager] = None


def get_secrets_manager() -> SecretsManager:
    """Get or create global secrets manager instance"""
    global _manager
    if _manager is None:
        _manager = SecretsManager()
    return _manager


def setup_secrets_interactive():
    """Run interactive secrets setup"""
    return SecretsManager.create_env_from_user()


def get_secret(key: str, secret_type: str = "api_key") -> Optional[str]:
    """Get a secret (smart, never asks twice)"""
    manager = get_secrets_manager()
    return manager.get(key, secret_type)


def require_secret(key: str, secret_type: str = "api_key") -> str:
    """Get a required secret (fail if not available)"""
    manager = get_secrets_manager()
    return manager.require_secret(key, secret_type)


def show_secrets_status():
    """Show which secrets are configured"""
    manager = get_secrets_manager()
    manager.print_status()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_secrets_interactive()
    elif len(sys.argv) > 1 and sys.argv[1] == "status":
        show_secrets_status()
    else:
        print("""
SECRETS MANAGER - Usage

python secrets_manager.py setup     - Interactive setup
python secrets_manager.py status    - Show configured secrets

Or use in code:
    from secrets_manager import get_secret, require_secret

    api_key = get_secret("ANTHROPIC_API_KEY")      # Ask if needed
    stripe = require_secret("STRIPE_SECRET_KEY")   # Fail if missing
""")
