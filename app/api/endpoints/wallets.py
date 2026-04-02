from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import WalletCreateResponse, WalletBalanceResponse, DepositRequest, DepositResponse, TransferRequest, TransferResponse
from app.services import WalletService

router = APIRouter(prefix="/api/wallets", tags=["wallets"])

def get_service(db: AsyncSession = Depends(get_db)) -> WalletService:
    return WalletService(db)

@router.post("", response_model=WalletCreateResponse)
async def create_wallet(service: WalletService = Depends(get_service)):
    return await service.create_wallet()

@router.get("/{wallet_id}/balance", response_model=WalletBalanceResponse)
async def get_balance(wallet_id: str, service: WalletService = Depends(get_service)):
    return await service.get_balance(wallet_id)

@router.post("/{wallet_id}/deposit", response_model=DepositResponse)
async def deposit(wallet_id: str, request: DepositRequest, service: WalletService = Depends(get_service)):
    return await service.deposit(wallet_id, request)

@router.post("/transfer", response_model=TransferResponse)
async def transfer(request: TransferRequest, service: WalletService = Depends(get_service)):
    return await service.transfer(request)
