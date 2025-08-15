from unittest.mock import AsyncMock, patch
import pytest
from sqlalchemy.exc import IntegrityError
from app.repository.accessors.dbase_accessor import Accessor


@pytest.mark.anyio
async def test_save_wallet_success(mock_app):
    accessor = Accessor(app=mock_app)
    accessor.logger = pytest.importorskip("logging").getLogger("test")

    mock_session = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock()

    with patch.object(accessor.app.db, "session", return_value=mock_session):
        result = await accessor.save_wallet(
            address="TQn9Y2khEsLJW1ChUyD7UvS4VZPjQ995Wf",
            trx_balance=100.5,
            bandwidth=50.0,
            energy=30.0
        )

    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()
    assert result is True

