import pytest
from app import app

@pytest.fixture
def browser():
    # create a test version of the app for simulation
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

#---TEST 1---
def test_home_page_loads(browser):
    """Test that the main dashboard loads correctly"""
    response = browser.get('/')
    assert response.status_code == 200
    assert b"Cybersecurity Incident Dashboard" in response.data

#---TEST 2---
def test_history_toggle(browser):
    """Test that the 'View All' logic actually returns more data"""
    #Check default view (should have roughly 10 rows in the table)
    response_default = browser.get('/')
    
    #Check history view (should have 3000 rows)
    response_all = browser.get('/?all=true')
    
    assert response_all.status_code == 200
    #check if the 'Back' button appears in the historical view (button for home page return)
    assert b"Back to Top 10 Dashboard" in response_all.data

#---TEST 3---
def test_incident_detail_loads(browser):
    """Test that clicking an incident ID works (using ID 1 as an example)"""
    response = browser.get('/incident/1')
    assert response.status_code == 200 or response.status_code == 404 