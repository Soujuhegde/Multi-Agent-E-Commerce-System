from fastapi import APIRouter

from src.agents.invoice.invoice_generator import (
    InvoiceGenerator
)

router = APIRouter(
    prefix="/invoice",
    tags=["Invoice"]
)


@router.post("/generate")
async def generate_invoice():

    invoice_number = (
        InvoiceGenerator
        .generate_invoice_number()
    )

    return {
        "success": True,
        "invoice_number": invoice_number
    }


@router.get("/{invoice_number}")
async def get_invoice(
    invoice_number: str
):

    return {
        "invoice_number": invoice_number,
        "status": "generated"
    }