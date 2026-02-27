#!/usr/bin/env python3
"""Simple script to populate a few secrets into HashiCorp Vault."""

import os
import sys

try:
    import hvac
except ImportError:
    sys.exit("Please install hvac (pip install hvac) before running this script.")


def main():
    # Vault configuration - using environment variables for flexibility
    vault_addr = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
    vault_token = os.environ.get("VAULT_TOKEN")

    if not vault_token:
        print("Error: VAULT_TOKEN environment variable is required.")
        sys.exit(1)

    client = hvac.Client(url=vault_addr, token=vault_token)

    if not client.is_authenticated():
        print("Failed to authenticate with Vault.")
        sys.exit(1)

    # define some example secrets
    secrets = {
        "secret/data/myapp/config": {"data": {"username": "admin", "password": "s3cr3t"}},
        "secret/data/myapp/api": {"data": {"api_key": "abcd1234"}},
        "secret/data/other/service": {"data": {"token": "xyz789"}},
    }

    for path, payload in secrets.items():
        try:
            client.secrets.kv.v2.create_or_update_secret(path=path.replace("secret/data/", ""), secret=payload["data"])
            print(f"Wrote secret to {path}")
        except Exception as err:
            print(f"Failed writing {path}: {err}")


if __name__ == "__main__":
    main()
