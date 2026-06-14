import os
import sys
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import Transaction, Category

def train_model(app):
    with app.app_context():
        transactions = Transaction.query.join(Category).all()
        
        X = [t.description for t in transactions if t.description]
        y = [t.category.name for t in transactions if t.description]
        
        if not X:
            print("No transactions found to train the model.")
            return

        print(f"Loaded {len(X)} transactions for training.")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create pipeline
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english', max_features=5000)),
            ('clf', MultinomialNB())
        ])

        print("Training model...")
        pipeline.fit(X_train, y_train)

        print("Evaluating model...")
        y_pred = pipeline.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc:.4f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred, zero_division=0))

        # Save model
        model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, 'categorizer.pkl')
        
        joblib.dump(pipeline, model_path)
        print(f"Model saved to {model_path}")

if __name__ == "__main__":
    app = create_app()
    train_model(app)
