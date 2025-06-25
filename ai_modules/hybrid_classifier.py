import joblib
import networkx as nx

class HybridClassifier:
    def __init__(self):
        self.rf_model = joblib.load("./models/random_forest.pkl")
        self.gnn_model = load_gnn_model()

    def predict(self, features):
        rf_score = self.rf_model.predict_proba([features])[0][1]
        gnn_score = self.gnn_model.predict(features)
        return 0.5 * rf_score + 0.5 * gnn_score

    @staticmethod
    def load_model():
        return HybridClassifier()
