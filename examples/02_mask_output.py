import inspect

from toolsuit import equip


def protect_pii(raw_data: dict) -> dict:
    """Filters the massive database returning only what the AI needs."""
    print("\n[TOOLSUIT] Masking heavy payload before returning to AI...")
    return {"status": "success", "user_name": raw_data.get("name")}


@equip(mask_output=protect_pii)
def fetch_user_profile(user_id: str):
    """Fetches a user profile from the database."""
    print(f"\n[SERVER EXECUTION] Fetching all records for '{user_id}'...")

    # Simulate a massive, sensitive database response
    massive_sensitive_data = {
        "id": user_id,
        "name": "Mohit",
        "hashed_password": "super_secret_sha256",
        "credit_card": "4242-1111-2222-3333",
        "account_balance": 5423.50,
        "logs": ["login_1", "login_2", "login_3"],
    }
    return massive_sensitive_data


if __name__ == "__main__":
    print("=== WHAT THE AI SEES ===")
    print(f"Schema: {inspect.signature(fetch_user_profile)}")

    print("\n=== AI EXECUTES THE TOOL ===")
    result = fetch_user_profile(user_id="usr_123")

    print("\n=== WHAT THE AI RECEIVES ===")
    print(result)
