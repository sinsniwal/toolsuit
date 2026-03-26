import inspect
from typing import Any, Dict

from toolsuit import equip


def get_db_session() -> Any:
    return "<secure_session_object>"


def filter_massive_payload(raw_data: Dict[str, Any]) -> Dict[str, str]:
    return {"status": "ok", "user": raw_data["id"]}


def resolve_fake_alias(alias: str) -> int:
    return {"usr_fake": 1482}.get(alias, 0)


@equip(
    hide=["db_session"],
    inject={"db_session": get_db_session},
    map_inputs={"user_id": resolve_fake_alias},
    mask_output=filter_massive_payload,
)
def fetch_secure_user(user_id: str, db_session: Any) -> Dict[str, Any]:
    print(
        f"\n[SERVER EXECUTION] Backend executing with Internal "
        f"ID {user_id} and DB {db_session}"
    )
    return {"id": user_id, "password": "super_secret_hash", "credit_card": "4242"}


if __name__ == "__main__":
    print("=== THE ALL-IN-ONE ENTERPRISE EXECUTION ===")
    print("\n1. Schema visible to the AI Framework:")
    print(f"   {inspect.signature(fetch_secure_user)}")

    print("\n2. AI Executes Function:")
    # AI blindly passes the string "usr_fake" without providing a DB connection
    print("   fetch_secure_user(user_id='usr_fake')")
    result = fetch_secure_user(user_id="usr_fake")

    print("\n3. What the AI receives back:")
    print(f"   {result}")
