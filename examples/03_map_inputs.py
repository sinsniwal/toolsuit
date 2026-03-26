import inspect
from toolsuit import equip

def resolve_alias_to_id(alias: str) -> int:
    """Simulates a DB lookup translating an AI's string alias to an internal integer."""
    mapping = {"agent_target_alpha": 9921}
    resolved_id = mapping.get(alias, 0)
    print(f"\n[TOOLSUIT] Translated AI alias '{alias}' -> Internal ID {resolved_id}")
    return resolved_id

@equip(map_inputs={"internal_user_id": resolve_alias_to_id})
def ban_user(internal_user_id: int):
    """Bans a malicious user from the platform."""
    print(f"[SERVER EXECUTION] Executing ban on internal database ID: {internal_user_id}")
    return {"banned": True}

if __name__ == "__main__":
    print("=== WHAT THE AI SEES ===")
    print(f"Schema: {inspect.signature(ban_user)}")
    
    print("\n=== AI EXECUTES THE TOOL ===")
    # The AI passes the string alias it discovered from a previous step
    ai_kwargs = {"internal_user_id": "agent_target_alpha"}
    print(f"AI passing arguments: {ai_kwargs}")
    
    result = ban_user(**ai_kwargs)
    print(f"\nResult: {result}")
