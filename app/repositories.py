from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Wallet
from typing import Optional

class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self) -> Wallet:
        wallet = Wallet(balance=0.00)
        self.session.add(wallet)
        await self.session.commit()
        await self.session.refresh(wallet)
        return wallet

    async def get_by_id(self, wallet_id: str) -> Optional[Wallet]:
        stmt = select(Wallet).where(Wallet.id == wallet_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def get_by_id_for_update(self, wallet_id: str) -> Optional[Wallet]:
        stmt = select(Wallet).where(Wallet.id == wallet_id).with_for_update()
        result = await self.session.execute(stmt)
        return result.scalars().first()
