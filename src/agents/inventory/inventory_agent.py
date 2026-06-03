from src.agents.base.base_agent import BaseAgent
from src.agents.base.agent_state import AgentState
from src.database.session import SessionLocal
from src.database.models import Product
from src.llm.sarvam_client import SarvamClient
from src.llm.prompts import PromptTemplates


class InventoryAgent(BaseAgent):

    def __init__(self):
        super().__init__("InventoryAgent")
        self.llm = SarvamClient()

    def execute(
        self,
        state: AgentState
    ) -> AgentState:

        self.log("Checking warehouse stock levels")

        query = state.get("user_query", "")

        db = SessionLocal()

        try:
            # 1. Fetch live product data from database
            products = db.query(Product).all()

            inventory_data = "\n".join([
                f"- {p.product_name} (Category: {p.category}): Price ₹{p.price:,.2f}, Stock: {p.stock_quantity} units"
                for p in products
            ])

            # 2. Query the LLM using the inventory prompt template
            prompt = PromptTemplates.INVENTORY_AGENT.format(
                query=query,
                inventory_data=inventory_data
            )

            llm_response = self.llm.generate(prompt)

            # 3. Store result status in state
            state["inventory_result"] = {
                "status": "success",
                "message": "Inventory checked successfully",
                "products_count": len(products)
            }

            if llm_response:
                state["final_response"] = llm_response.strip()
            else:
                state["final_response"] = (
                    f"Stock levels verified. Total products in catalog: {len(products)}."
                )

        except Exception as exc:
            self.log(f"Error checking inventory: {exc}")
            state["error"] = str(exc)

        finally:
            db.close()

        return state