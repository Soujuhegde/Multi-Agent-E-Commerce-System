from datetime import datetime
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

            # 5. Build HTML Invoice matching exact frontend design
            subtotal = invoice.total_amount - invoice.tax_amount
            date_str = datetime.utcnow().strftime("%d %b %Y, %H:%M UTC")
            
            html_invoice = f"""
        <div class="premium-card" style="
            border-top:3px solid #16a34a !important;
            max-width:580px; margin:0 auto; background:#ffffff;
        ">
            <!-- Header -->
            <div style="text-align:center; margin-bottom:24px;">
                <div style="
                    display:inline-flex; align-items:center; justify-content:center;
                    width:44px; height:44px; border-radius:50%;
                    background:#f0fdf4; border:1.5px solid #16a34a;
                    font-size:20px; margin-bottom:12px;">✓</div>
                <h2 style="color:#16a34a; margin:0 0 4px 0; font-size:16px; font-weight:700;">
                    Invoice Generated
                </h2>
                <p style="color:#475569; font-size:12.5px; margin:0;">Aether E-Commerce Platform</p>
            </div>
            <!-- Meta -->
            <div style="font-size:13px; margin-bottom:20px; color:#0f172a;">
                <div style="display:flex; justify-content:space-between;
                            border-bottom:1px solid #f1f5f9; padding-bottom:6px; margin-bottom:6px;">
                    <span style="color:#475569;">Invoice ID</span>
                    <strong>{invoice.invoice_number}</strong>
                </div>
                <div style="display:flex; justify-content:space-between;
                            border-bottom:1px solid #f1f5f9; padding-bottom:6px; margin-bottom:6px;">
                    <span style="color:#475569;">Date</span>
                    <span>{date_str}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#475569;">Customer</span>
                    <span>{customer_name}</span>
                </div>
            </div>
            <!-- Items table -->
            <table style="width:100%; border-collapse:collapse; margin-bottom:16px;">
                <thead>
                    <tr style="border-bottom:1.5px solid #e2e8f0;">
                        <th style="padding-bottom:7px; text-align:left; font-size:11px;
                                   text-transform:uppercase; letter-spacing:0.5px;
                                   color:#475569; font-weight:600;">Product</th>
                        <th style="padding-bottom:7px; text-align:center; font-size:11px;
                                   text-transform:uppercase; letter-spacing:0.5px;
                                   color:#475569; font-weight:600;">Qty</th>
                        <th style="padding-bottom:7px; text-align:right; font-size:11px;
                                   text-transform:uppercase; letter-spacing:0.5px;
                                   color:#475569; font-weight:600;">Unit Price</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom:1px solid #f1f5f9;">
                        <td style="padding:7px 0; color:#0f172a; font-size:13px;">{matched_product.product_name}</td>
                        <td style="padding:7px 0; text-align:center; color:#475569; font-size:13px;">1</td>
                        <td style="padding:7px 0; text-align:right; color:#0f172a; font-size:13px;">₹{matched_product.price:,.2f}</td>
                    </tr>
                </tbody>
            </table>
            <!-- Totals -->
            <div style="background:#f0fdf4; border-radius:10px; padding:14px 16px;
                        border:1px solid #bbf7d0;">
                <div style="display:flex; justify-content:space-between;
                            font-size:13px; margin-bottom:5px; color:#475569;">
                    <span>Subtotal</span>
                    <span style="color:#0f172a;">₹{subtotal:,.2f}</span>
                </div>
                <div style="display:flex; justify-content:space-between;
                            font-size:13px; margin-bottom:8px; color:#475569;">
                    <span>GST (18%)</span>
                    <span style="color:#0f172a;">₹{invoice.tax_amount:,.2f}</span>
                </div>
                <hr style="border:none; border-top:1px solid #bbf7d0; margin:8px 0;">
                <div style="display:flex; justify-content:space-between;
                            font-size:15px; font-weight:700; color:#16a34a;">
                    <span>Grand Total</span>
                    <span>₹{invoice.total_amount:,.2f}</span>
                </div>
            </div>
            <p style="text-align:center; font-size:11.5px; color:#94a3b8;
                      margin:16px 0 0 0; letter-spacing:0.3px;">
                ✓ Electronically generated. No physical signature required.
            </p>
        </div>
        """

            # 6. Save results to state
            state["invoice_result"] = {
                "status": "success",
                "invoice_number": invoice.invoice_number,
                "customer_name": customer_name,
                "total_amount": invoice.total_amount,
                "tax_amount": invoice.tax_amount
            }

            state["final_response"] = html_invoice.replace("\n", "").strip()

        except Exception as exc:
            self.log(f"Error billing invoice: {exc}")
            state["error"] = str(exc)

        finally:
            db.close()

        return state