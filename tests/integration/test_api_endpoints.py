import pytest
from unittest.mock import AsyncMock, patch
from app.api.endpoints.models import WalletInfoResponse
from datetime import datetime

@pytest.mark.anyio
async def test_wallet_flow(client):
    with patch(
        "app.services.tron_service.tron_service.TronService.get_wallet_data",
        new_callable=AsyncMock
    ) as mock_get_wallet, patch(
        "app.repository.accessors.dbase_accessor.Accessor.save_wallet",
        new_callable=AsyncMock
    ) as mock_save_wallet:

        mock_get_wallet.return_value = WalletInfoResponse(
            address="TMyaAB712h2QKpY4NpYH8x6n2j671j8j9j",
            trx_balance=100.0,
            bandwidth=50.0,
            energy=30.0,
            updated_at=datetime.now()
        )
        mock_save_wallet.return_value = True

        response = await client.post("/api/wallet", json={"address": "TMyaAB712h2QKpY4NpYH8x6n2j671j8j9j"})

        assert response.status_code == 200, f"Got {response.status_code}: {response.text}"
        data = response.json()

        assert data["address"] == "TMyaAB712h2QKpY4NpYH8x6n2j671j8j9j"
        assert data["trx_balance"] == 100.0
        assert data["bandwidth"] == 50.0
        assert data["energy"] == 30.0

        mock_get_wallet.assert_called_once_with(address="TMyaAB712h2QKpY4NpYH8x6n2j671j8j9j")
        mock_save_wallet.assert_called_once_with(
            address="TMyaAB712h2QKpY4NpYH8x6n2j671j8j9j",
            trx_balance=100.0,
            bandwidth=50.0,
            energy=30.0
        )