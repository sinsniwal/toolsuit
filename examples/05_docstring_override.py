import inspect

from toolsuit import equip


def get_user_db_session():
    """Simulates fetching a secure DB session."""
    return "<secure_db_session>"


@equip(
    hide=["db_session"],
    inject={"db_session": get_user_db_session},
    description="Fetches a user record.",
)
def fetch_user(user_id: str, db_session: str):
    """
    Fetches a user record from the database using the provided session.

    Args:
        user_id (str): The unique identifier of the user to fetch.
        db_session (str): The database session or connection object.

    Returns:
        The user record corresponding to the given user_id.
    """
    print(f"[SERVER EXECUTION] Fetching user '{user_id}' with session: {db_session}")
    return {"user_id": user_id, "status": "found"}


if __name__ == "__main__":
    print("=== WHAT THE AI SEES ===")
    print(f"Schema: {inspect.signature(fetch_user)}")
    print(f"Docstring: {fetch_user.__doc__}")

    print("\n=== AI EXECUTES THE TOOL ===")
    ai_kwargs = {"user_id": "usr_42"}
    print(f"AI passing arguments: {ai_kwargs}")

    result = fetch_user(**ai_kwargs)
    print(f"\nResult: {result}")
