import inspect
from toolsuit import equip

def get_secure_api_key() -> str:
    """Simulates fetching a sensitive API key from an environment variable."""
    return "sk_live_super_secret_123"

@equip(
    hide=["api_key"], 
    inject={"api_key": get_secure_api_key}
)
def charge_credit_card(amount: float, api_key: str):
    """Charges a user's credit card."""
    print(f"[SERVER EXECUTION] Processing charge of ${amount} using key: {api_key}")
    return {"status": "charge_successful"}

if __name__ == "__main__":
    print("=== WHAT THE AI SEES ===")
    print(f"Schema: {inspect.signature(charge_credit_card)}")
    
    print("\n=== AI EXECUTES THE TOOL ===")
    # Notice the AI does not provide the api_key!
    ai_kwargs = {"amount": 50.0}
    print(f"AI passing arguments: {ai_kwargs}")
    
    result = charge_credit_card(**ai_kwargs)
    print(f"\nResult: {result}")
