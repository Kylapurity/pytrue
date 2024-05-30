#!/usr/bin/python3
""" Helpers functions for working with refresh tokens"""
from models.refresh_token import RefreshToken
from models import db
import secrets


def grantAuthenticatedUser(user):
    """GrantAuthenticatedUser creates a refresh token for the provided user."""
    return createRefreshToken(user)

def grantRefreshTokenSwap(user_id, token: RefreshToken):
    """GrantRefreshTokenSwap swaps a refresh token for a new one, revoking the provided token."""
    new_token = createRefreshToken(user_id)
    RefreshToken.update(token.id, revoked=True)
    return new_token

def logout(user_id: str):
    """Logout deletes all refresh tokens for a user."""
    stmt = RefreshToken.__table__.delete().where(RefreshToken.user_id==user_id)
    db.session.execute(stmt)
    db.session.commit()

def createRefreshToken(user_id: str):
    """create Refresh Token"""
    token = secrets.token_urlsafe(16)
    rt = RefreshToken(user_id=user_id, token=token, revoked=False)
    rt.save()
    return token

