from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID
from app.core.config import settings

# This tells FastAPI where the token URL is, but Keycloak handles it.
# We won't implement this URL ourselves.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configure the Keycloak client
keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency to get the current user from a token.
    Validates the token and returns the user info payload.
    """
    try:
        # Decode and validate the token
        return keycloak_openid.decode_token(token)
    except Exception as e:
        # If token is invalid, expired, or malformed
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(required_role: str):
    """
    A dependency factory that returns a dependency checking for a specific role.
    """
    async def role_checker(user: dict = Depends(get_current_user)):
        try:
            # Keycloak roles are nested under 'realm_access' or 'resource_access'
            user_roles = user.get("realm_access", {}).get("roles", [])
            if required_role not in user_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Forbidden: User does not have the required '{required_role}' role.",
                )
            return user
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: Could not validate user roles.",
            )
    return role_checker