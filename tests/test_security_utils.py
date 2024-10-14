import pytest
from datetime import timedelta
from jose import jwt
from policy_core.SupportUtils.security_utils.oauth2_security import AuthService

@pytest.fixture
def mock_settings():
    """
    Fixture to mock application settings required for AuthService.
    
    GIVEN: Mocked application settings with secret key, algorithm, and token expiration times.
    """
    class MockSettings:
        SECRET_KEY = "testsecret"
        ALGORITHM = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES = 15
        REFRESH_TOKEN_EXPIRE_DAYS = 7
    return MockSettings()

@pytest.fixture
def auth_service(mock_settings):
    """
    Fixture to initialize AuthService with mocked settings.
    
    GIVEN: An AuthService instance initialized with mock settings.
    """
    return AuthService(mock_settings)

def test_verify_password(auth_service):
    """
    Test to verify password matching and non-matching.
    
    GIVEN: A hashed password.
    WHEN: The password is verified using the correct and incorrect values.
    THEN: The result should be True for the correct password and False for an incorrect one.
    """
    hashed_password = auth_service.pwd_context.hash("testpassword")

    # WHEN: Correct password is verified
    assert auth_service.verify_password("testpassword", hashed_password) is True

    # WHEN: Incorrect password is verified
    assert auth_service.verify_password("wrongpassword", hashed_password) is False

def test_authenticate_user(auth_service):
    """
    Test user authentication with correct and incorrect credentials.
    
    GIVEN: A set of credentials.
    WHEN: Authenticate a user with valid and invalid username/password combinations.
    THEN: Authentication should succeed for correct credentials and fail for incorrect ones.
    """
    
    # WHEN: User does not exist
    assert auth_service.authenticate_user("wrongusername", "TestUserPassword") is None

    # WHEN: User exists with wrong password
    assert auth_service.authenticate_user("testusername", "wrongpassword") is None

def test_create_access_token(auth_service):
    """
    Test access token creation and validation.
    
    GIVEN: A set of user data (sub: testusername).
    WHEN: Access token is created without custom expiration time.
    THEN: The token should be valid, containing the correct subject and expiration field.
    """
    data = {"sub": "testusername"}
    
    # WHEN: Token is created
    token = auth_service.create_access_token(data)
    
    # THEN: Token should be decoded and validated
    decoded_token = jwt.decode(token, auth_service.SECRET_KEY, algorithms=[auth_service.ALGORITHM])
    assert decoded_token["sub"] == "testusername"
    assert "exp" in decoded_token

def test_create_access_token_with_expiration(auth_service):
    """
    Test access token creation with custom expiration time.
    
    GIVEN: A set of user data (sub: testusername) and a custom expiration time.
    WHEN: Access token is created with custom expiration (10 minutes).
    THEN: The token should be valid, containing the correct subject and expiration field.
    """
    data = {"sub": "testusername"}
    expires_delta = timedelta(minutes=10)
    
    # WHEN: Token is created with custom expiration
    token = auth_service.create_access_token(data, expires_delta)
    
    # THEN: Token should be decoded and validated
    decoded_token = jwt.decode(token, auth_service.SECRET_KEY, algorithms=[auth_service.ALGORITHM])
    assert decoded_token["sub"] == "testusername"
    assert "exp" in decoded_token

def test_create_refresh_token(auth_service):
    """
    Test refresh token creation and validation.
    
    GIVEN: A set of user data (sub: testusername).
    WHEN: Refresh token is created without custom expiration time.
    THEN: The token should be valid, containing the correct subject and expiration field.
    """
    data = {"sub": "testusername"}
    
    # WHEN: Token is created
    token = auth_service.create_refresh_token(data)
    
    # THEN: Token should be decoded and validated
    decoded_token = jwt.decode(token, auth_service.SECRET_KEY, algorithms=[auth_service.ALGORITHM])
    assert decoded_token["sub"] == "testusername"
    assert "exp" in decoded_token

def test_create_refresh_token_with_expiration(auth_service):
    """
    Test refresh token creation with custom expiration time.
    
    GIVEN: A set of user data (sub: testusername) and a custom expiration time.
    WHEN: Refresh token is created with custom expiration (5 days).
    THEN: The token should be valid, containing the correct subject and expiration field.
    """
    data = {"sub": "testusername"}
    expires_delta = timedelta(days=5)
    
    # WHEN: Token is created with custom expiration
    token = auth_service.create_refresh_token(data, expires_delta)
    
    # THEN: Token should be decoded and validated
    decoded_token = jwt.decode(token, auth_service.SECRET_KEY, algorithms=[auth_service.ALGORITHM])
    assert decoded_token["sub"] == "testusername"
    assert "exp" in decoded_token
