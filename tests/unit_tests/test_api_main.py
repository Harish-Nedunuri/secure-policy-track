from fastapi.testclient import TestClient
from main import app

# Create a TestClient instance for the FastAPI app
client = TestClient(app)

def test_home_view():
    """
    Given the FastAPI app is running,
    When a GET request is sent to the home endpoint (/),
    Then the response should return a status code 200 and contain the text 'Running!' in the HTML.
    """
    
    # WHEN: Send a GET request to the home endpoint
    response = client.get("/")
    print(response)

    # THEN: Verify the status code is 200 (OK)
    assert response.status_code == 200

    # THEN: Verify that the response content-type is HTML
    assert response.headers["content-type"] == "text/html; charset=utf-8"

    print("Response",response.text)


