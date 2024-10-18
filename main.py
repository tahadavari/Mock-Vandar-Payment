import random
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel

app = FastAPI()


class InitiatePaymentRequest(BaseModel):
    api_key: str
    amount: float
    callback_url: str
    factorNumber: str
    mobile_number: Optional[str] = None
    description: Optional[str] = None
    comment: Optional[str] = None


class InitiatePaymentResponse(BaseModel):
    status: int
    token: Optional[str] = None


class VerifyPaymentRequest(BaseModel):
    api_key: str
    token: str


class VerifyPaymentResponse(BaseModel):
    status: int


payments = {}


@app.post("/send")
async def initiate_payment(request: InitiatePaymentRequest):
    if request.api_key != "your_valid_api_key":
        return JSONResponse(status_code=400, content={
            "status": 0,
            "errors": "Invalid API Key"
        })

    token = f"token_{random.randint(1000, 9999)}"
    payments[token] = {
        "amount": request.amount,
        "status": "pending",
        "callback_url": request.callback_url,
        "factorNumber": request.factorNumber,
        "mobile_number": request.mobile_number,
        "description": request.description,
        "comment": request.comment,
    }

    response = InitiatePaymentResponse(status=1, token=token)
    return response


@app.post("/verify")
async def verify_payment(request: VerifyPaymentRequest):
    payment = payments.get(request.token)
    if not payment:
        return JSONResponse(status_code=400, content={
            "status": 0,
            "errors": "Invalid Token"
        })

    if payment["status"] == "pending":
        payment_status = random.choice(["paid", "failed"])
        payment["status"] = payment_status

    if payment["status"] == "paid":
        response = VerifyPaymentResponse(status=1)
    elif payment["status"] == "failed":
        response = VerifyPaymentResponse(status=2)
    else:
        response = VerifyPaymentResponse(status=0, errors="Unknown Error")

    return response


@app.get("/payment/{token}")
async def payment_page(token: str):
    payment = payments.get(token)
    if not payment:
        raise HTTPException(status_code=404, detail="Token not found")

    payment["status"] = "paid"
    callback_url = payment["callback_url"]
    redirect_url = f"{callback_url}?token={token}"
    print(redirect_url)
    return RedirectResponse(url=redirect_url)
