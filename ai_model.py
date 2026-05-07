def train_model():
    # Dummy model (upgrade later)
    return "model"

def predict_traffic(model, traffic_data):
    prediction = {}

    for edge, count in traffic_data.items():
        prediction[edge] = count * 1.5  # AI logic

    return prediction

def get_priority_edge(predicted_data):
    if not predicted_data:
        return None

    return max(predicted_data, key=predicted_data.get)