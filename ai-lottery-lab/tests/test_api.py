from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_predict_endpoint():
    response = client.get('/api/predict')
    assert response.status_code == 200
    body = response.json()
    assert 'ranking' in body
    assert len(body['ranking']) > 0


def test_train_endpoint():
    response = client.post('/api/train', json={"dataset": "100", "models": ["markov", "bayes", "rf", "xgb", "lgb", "lstm"]})
    assert response.status_code == 200
    body = response.json()
    assert body['status'] == 'completed'
    assert len(body['trained_models']) == 6


def test_backtest_endpoint():
    response = client.get('/api/backtest')
    assert response.status_code == 200
    body = response.json()
    assert 'top5' in body
    assert 'random_baseline' in body


def test_analytics_endpoint():
    response = client.get('/api/analytics?limit=100')
    assert response.status_code == 200
    body = response.json()
    assert 'total_draws' in body
    assert 'missing_matrix' in body
    assert 'tail_dist' in body
    assert len(body['missing_matrix']) == 49


def test_combo_test_endpoint():
    response = client.post('/api/analytics/combo-test', json={"numbers": [17, 42, 8, 31, 23], "limit": 100, "bet_per_number": 10.0, "odds": 48.0})
    assert response.status_code == 200
    body = response.json()
    assert 'combo_numbers' in body
    assert 'hits' in body
    assert 'roi' in body
    assert 'net_profit' in body


