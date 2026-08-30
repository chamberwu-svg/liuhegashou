import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from app.models.markov import MarkovPredictor
from app.models.bayesian import BayesianPredictor
from app.models.random_forest import RandomForestPredictor
from app.models.xgboost_model import XGBoostPredictor
from app.models.lightgbm_model import LightGBMPredictor
from app.models.lstm import LSTMPredictor
from app.feature.engineering import build_tabular_dataset, extract_draw_features
from app.services.pipeline import PredictionPipeline
from app.ensemble.fusion import fuse_scores
from app.ensemble.consensus import calculate_consensus


def test_markov_predict_returns_probability_vector():
    history = [12, 17, 23, 8, 42, 31, 17, 15, 9, 22, 11, 33, 25, 40, 7, 18, 29, 44]
    model = MarkovPredictor(order=1)
    model.train(history)
    prediction = model.predict(history)
    assert len(prediction) == 49
    assert sum(prediction.values()) > 0


def test_bayesian_predict_works():
    history = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 5
    model = BayesianPredictor().train(history)
    scores = model.predict()
    assert len(scores) == 49
    assert sum(scores.values()) > 0


def test_all_ml_models_predict():
    history = [i % 49 + 1 for i in range(60)]
    X_train, y_train = build_tabular_dataset(history, min_history=20)
    x_curr = extract_draw_features(history)

    rf = RandomForestPredictor(n_estimators=10).train(X_train, y_train)
    rf_pred = rf.predict([x_curr])
    assert len(rf_pred) == 49

    xgb = XGBoostPredictor().train(X_train, y_train)
    xgb_pred = xgb.predict([x_curr])
    assert len(xgb_pred) == 49

    lgb = LightGBMPredictor().train(X_train, y_train)
    lgb_pred = lgb.predict([x_curr])
    assert len(lgb_pred) == 49

    lstm = LSTMPredictor(sequence_length=10).train(history, epochs=2)
    lstm_pred = lstm.predict(history)
    assert len(lstm_pred) == 49


def test_pipeline_runs_all_models():
    history = [i % 49 + 1 for i in range(50)]
    pipeline = PredictionPipeline(history)
    ranking = pipeline.run()
    assert len(ranking) > 0
    assert "consensus" in ranking[0]
    assert "score" in ranking[0]


def test_fusion_and_consensus_are_formed():
    model_scores = {
        "markov": {17: 0.80, 42: 0.70},
        "bayes": {17: 0.90, 42: 0.65},
        "rf": {17: 0.85, 42: 0.60},
        "xgb": {17: 0.95, 42: 0.75},
        "lgb": {17: 0.88, 42: 0.72},
        "lstm": {17: 0.82, 42: 0.68},
    }
    fused = fuse_scores(model_scores)
    assert fused[0]["number"] == 17
    consensus = calculate_consensus(model_scores)
    assert any(item["number"] == 17 for item in consensus)

