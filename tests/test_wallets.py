import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_wallet_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/wallets")
        assert response.status_code == 200
        wallet_a_id = response.json()["walletId"]

        response = await ac.post(f"/api/wallets/{wallet_a_id}/deposit", json={"amount": 100.50})
        assert response.status_code == 200
        assert float(response.json()["balance"]) == 100.50

        response = await ac.post("/api/wallets")
        wallet_b_id = response.json()["walletId"]

        response = await ac.post("/api/wallets/transfer", json={
            "fromWalletId": wallet_a_id,
            "toWalletId": wallet_b_id,
            "amount": 50.00
        })
        assert response.status_code == 200
        assert response.json()["status"] == "success"

        res_a = await ac.get(f"/api/wallets/{wallet_a_id}/balance")
        res_b = await ac.get(f"/api/wallets/{wallet_b_id}/balance")
        
        assert float(res_a.json()["balance"]) == 50.50
        assert float(res_b.json()["balance"]) == 50.00
