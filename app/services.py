from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
import logging
from app.repositories import WalletRepository
from app.schemas import WalletCreateResponse, WalletBalanceResponse, DepositRequest, DepositResponse, TransferRequest, TransferResponse

logger = logging.getLogger(__name__)

class WalletService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = WalletRepository(db)

    async def create_wallet(self) -> WalletCreateResponse:
        wallet = await self.repo.create()
        logger.info(f"Created wallet {wallet.id}")
        return WalletCreateResponse(walletId=wallet.id, balance=wallet.balance)

    async def get_balance(self, wallet_id: str) -> WalletBalanceResponse:
        wallet = await self.repo.get_by_id(wallet_id)
        if not wallet:
            logger.warning(f"Wallet {wallet_id} not found")
            raise HTTPException(status_code=404, detail="Wallet not found")
        return WalletBalanceResponse(walletId=wallet.id, balance=wallet.balance)

    async def deposit(self, wallet_id: str, request: DepositRequest) -> DepositResponse:
        async with self.db.begin():
            wallet = await self.repo.get_by_id_for_update(wallet_id)
            if not wallet:
                raise HTTPException(status_code=404, detail="Wallet not found")
            
            wallet.balance += request.amount
            await self.db.commit()
            
            logger.info(f"Deposited {request.amount} to wallet {wallet.id}")
            return DepositResponse(walletId=wallet.id, balance=wallet.balance)

    async def transfer(self, request: TransferRequest) -> TransferResponse:
        if request.fromWalletId == request.toWalletId:
            raise HTTPException(status_code=400, detail="Cannot transfer to the same wallet")

        first_id, second_id = sorted([request.fromWalletId, request.toWalletId])

        async with self.db.begin():
            first_wallet = await self.repo.get_by_id_for_update(first_id)
            if not first_wallet:
                raise HTTPException(status_code=404, detail=f"Wallet {first_id} not found")
            
            second_wallet = await self.repo.get_by_id_for_update(second_id)
            if not second_wallet:
                raise HTTPException(status_code=404, detail=f"Wallet {second_id} not found")

            from_wallet = first_wallet if first_wallet.id == request.fromWalletId else second_wallet
            to_wallet = second_wallet if second_wallet.id == request.toWalletId else first_wallet

            if from_wallet.balance < request.amount:
                raise HTTPException(status_code=422, detail="Insufficient balance")

            from_wallet.balance -= request.amount
            to_wallet.balance += request.amount
            
            await self.db.commit()
            
            logger.info(f"Transferred {request.amount} from {from_wallet.id} to {to_wallet.id}")
            return TransferResponse(status="success")
