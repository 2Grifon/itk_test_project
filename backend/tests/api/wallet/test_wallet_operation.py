import uuid
from decimal import Decimal

from fastapi import HTTPException, status

from tests.conftest import FakeWallet


def test_deposit_ok(client, fake_service):
    fake_service.wallet = FakeWallet("150.00")

    response = client.post(
        f"/wallets/{fake_service.wallet.id}/operation",
        json={"operation_type": "DEPOSIT", "amount": "50.00"},
    )

    assert response.status_code == 200
    assert Decimal(response.json()["balance"]) == Decimal("150.00")


def test_withdraw_ok(client, fake_service):
    fake_service.wallet = FakeWallet("70.00")

    response = client.post(
        f"/wallets/{fake_service.wallet.id}/operation",
        json={"operation_type": "WITHDRAW", "amount": "30.00"},
    )

    assert response.status_code == 200
    assert Decimal(response.json()["balance"]) == Decimal("70.00")


def test_withdraw_insufficient_funds(client, fake_service):
    def raise_400(wallet_id, operation):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds",
        )

    fake_service.perform_operation = raise_400

    response = client.post(
        f"/wallets/{uuid.uuid4()}/operation",
        json={"operation_type": "WITHDRAW", "amount": "9999.00"},
    )

    assert response.status_code == 400
    assert "Insufficient funds" in response.json()["detail"]


def test_operation_wallet_not_found(client, fake_service):
    def raise_404(wallet_id, operation):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found",
        )

    fake_service.perform_operation = raise_404

    response = client.post(
        f"/wallets/{uuid.uuid4()}/operation",
        json={"operation_type": "DEPOSIT", "amount": "10.00"},
    )

    assert response.status_code == 404


def test_operation_invalid_type(client):
    response = client.post(
        f"/wallets/{uuid.uuid4()}/operation",
        json={"operation_type": "INVALID", "amount": "10.00"},
    )

    assert response.status_code == 422


def test_operation_negative_amount(client):
    response = client.post(
        f"/wallets/{uuid.uuid4()}/operation",
        json={"operation_type": "DEPOSIT", "amount": "-1.00"},
    )

    assert response.status_code == 422
