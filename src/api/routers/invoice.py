from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.session import SessionLocal
from src.schemas.invoice import InvoiceCreateRequest, InvoiceResponse
from src.services.invoice_service import InvoiceService

router = APIRouter(
    prefix="/invoice",
    tags=["Invoice"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/generate", response_model=InvoiceResponse)
async def generate_invoice(
    request: InvoiceCreateRequest,
    db: Session = Depends(get_db)
):

    try:
        invoice = InvoiceService.generate_invoice(db, request)
        return invoice
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {str(exc)}")


@router.get("/{invoice_number}")
async def get_invoice(
    invoice_number: str,
    db: Session = Depends(get_db)
):

    invoice = InvoiceService.get_invoice(db, invoice_number)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice