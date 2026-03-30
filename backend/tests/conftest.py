import uuid
from decimal import Decimal
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.wallet.routes import router
from app.modules.wallet.services import WalletService

app = FastAPI()
app.include_router(router)


class FakeWallet:
    def __init__(self, balance: str = "100.00"):
        self.id = uuid.uuid4()
        self.balance = Decimal(balance)


class FakeWalletService:
    def __init__(self):
        self.wallet = FakeWallet()

    async def get_wallet(self, wallet_id):
        return self.wallet

    async def perform_operation(self, wallet_id, operation):
        return self.wallet


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def fake_service():
    service = FakeWalletService()
    app.dependency_overrides[WalletService] = lambda: service
    yield service
    app.dependency_overrides.clear()
