from src.agents.base.base_agent import BaseAgent
from src.agents.base.agent_state import AgentState
from src.database.session import SessionLocal
from src.database.models import Product
from src.schemas.invoice import InvoiceCreateRequest, InvoiceItemRequest
from src.llm.sarvam_client import SarvamClient
from src.llm.prompts import PromptTemplates


class InvoiceAgent(BaseAgent):

    def __init__(self):
        super().__init__("InvoiceAgent")
        self.llm = SarvamClient()

    def execute(
        self,
        state: AgentState
    ) -> AgentState:

        # Import dynamically here to avoid package circular dependencies
        from src.services.invoice_service import InvoiceService

        self.log("Billing customer order and generating tax invoice")

        query = state.get("user_query", "")

        db = SessionLocal()

        try:
            # 1. Parse target product name from the database matching the user's query
            products = db.query(Product).all()
            matched_product = None

            for p in products:
                if p.product_name.lower() in query.lower():
                    matched_product = p
                    break

            if not matched_product:
                # Default fallback if no specific product is found
                matched_product = db.query(Product).first()
                if not matched_product:
                    state["error"] = "No products exist to bill"
                    return state

            # 2. Extract customer name from query: "for Rohan Malhotra" -> "Rohan Malhotra"
            customer_name = "Walk-in Customer"
            if "for " in query:
                parts = query.split("for ")
                if len(parts) > 1:
                    # Take the customer segment
                    words = parts[1].split(" ")
                    if len(words) > 1:
                        customer_name = f"{words[0]} {words[1]}".strip(",")
                    else:
                        customer_name = words[0].strip(",")

            # 3. Verify stock availability
            if matched_product.stock_quantity < 1:
                state["error"] = f"Product '{matched_product.product_name}' is out of stock."
                return state

            # 4. Generate persistent Invoice & InvoiceItem
            req = InvoiceCreateRequest(
                customer_name=customer_name,
                items=[
                    InvoiceItemRequest(
                        product_id=matched_product.id,
                        quantity=1
                    )
                ]
            )

            invoice = InvoiceService.generate_invoice(db, req)

            # 5. Get AI invoice summary
            prompt = PromptTemplates.INVOICE_AGENT.format(
                customer=customer_name,
                products=f"- 1x {matched_product.product_name} @ ₹{matched_product.price:,.2f}",
                total=f"₹{invoice.total_amount:,.2f} (includes ₹{invoice.tax_amount:,.2f} GST)"
            )

            llm_response = self.llm.generate(prompt)

            # 6. Save results to state
            state["invoice_result"] = {
                "status": "success",
                "invoice_number": invoice.invoice_number,
                "customer_name": customer_name,
                "total_amount": invoice.total_amount,
                "tax_amount": invoice.tax_amount
            }

            if llm_response:
                state["final_response"] = llm_response.strip()
            else:
                state["final_response"] = (
                    f"Invoice {invoice.invoice_number} created successfully for {customer_name}."
                )

        except Exception as exc:
            self.log(f"Error billing invoice: {exc}")
            state["error"] = str(exc)

        finally:
            db.close()

        return state