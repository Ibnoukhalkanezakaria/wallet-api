from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

class WalletCreateResponse(BaseModel):
    walletId: str
    balance: Decimal

class WalletBalanceResponse(BaseModel):
    walletId: str
    balance: Decimal

class DepositRequest(BaseModel):
    amount: Decimal = Field(gt=0, description="Amount must be positive")

class DepositResponse(BaseModel):
    walletId: str
    balance: Decimal

class TransferRequest(BaseModel):
    fromWalletId: str
    toWalletId: str
    amount: Decimal = Field(gt=0, description="Amount must be positive")

class TransferResponse(BaseModel):
    status: str
