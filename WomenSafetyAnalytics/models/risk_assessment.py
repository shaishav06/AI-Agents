from sklearn.ensemble import RandomForestClassifier

def train_risk_model(X, y):
    """Train a risk assessment model."""
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

def predict_risk(model, X_new):
    """Predict risk level for new data."""
    return model.predict(X_new)
