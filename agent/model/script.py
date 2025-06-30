import json
import re
import joblib
import os
import spacy
from langdetect import detect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

# Load fine-tuned spaCy NER model
nlp = spacy.load("agent/student_ner_model")

offensive_keywords = {"idiot", "stupid", "nonsense", "chutiya"}

# Common typo corrections
typo_corrections = {
    "fass": "fess",
    "fees": "fess",
    "fee": "fess"
}

class StudentInfoModel:
    def __init__(self):
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(2, 4))),
            ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
        ])

        self.valid_intents = {
            'get_student_info',
            'get_Students_by_class',
            'get_all_pending_fess',
            'get_pending_fess_by_class',
            'get_section_by_class',
            
        }

    def load_data(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f if line.strip()]

        X, y_intent, y_entities = [], [], []

        for item in data:
            X.append(item['prompt'])
            completion = json.loads(item['completion'])
            y_intent.append(completion['intent'])

            if 'name' in completion:
                y_entities.append(('name', completion['name']))
            elif 'class' in completion:
                y_entities.append(('class', completion['class']))
            elif 'fess' in completion:
                y_entities.append(('fess', completion['fess']))

        return X, y_intent, y_entities

    def train(self, X, y):
        self.model.fit(X, y)

    def autocorrect_text(self, text):
        for wrong, right in typo_corrections.items():
            text = re.sub(rf"\\b{wrong}\\b", right, text, flags=re.IGNORECASE)
        return text

    def detect_offensive(self, text):
        for word in offensive_keywords:
            if word in text.lower():
                return True
        return False

    def detect_language(self, text):
        try:
            return detect(text)
        except:
            return "unknown"

    def extract_entities(self, text, intent):
        entities = {}
        doc = nlp(text)

        for ent in doc.ents:
            if ent.label_ == "NAME":
                entities['name'] = ent.text.lower()
            elif ent.label_ == "CLASS":
                entities['class'] = ent.text
            elif ent.label_ == "FESS":
                entities['fess'] = 'fess'

        # Heuristic fallback for get_section_by_class
        if intent == 'get_section_by_class' and 'class' not in entities:
            match = re.search(r'class\s*(\d+)', text.lower())
            if match:
                entities['class'] = match.group(1)

        return entities

    def predict(self, text):
        print(f"\n\033[94m[PREDICT]\033[0m Input: {text}")

        if self.detect_offensive(text):
            print("\033[91m[BLOCKED]\033[0m Offensive content detected.")
            return {"error": "Offensive input"}

        lang = self.detect_language(text)
        print(f"\033[94m[LANGUAGE]\033[0m Detected language: {lang}")

        text = self.autocorrect_text(text)
        intent = self.model.predict([text])[0]

        if intent not in self.valid_intents:
            print(f"\033[91m[ERROR]\033[0m Unknown intent detected: {intent}")
            return {"intent": "unknown"}

        print(f"\033[94m[PREDICT]\033[0m Intent detected: {intent}")
        entities = self.extract_entities(text, intent)

        if not entities:
            print("\033[93m[WARNING]\033[0m No entities extracted.")

        print(f"\033[94m[PREDICT]\033[0m Extracted entities: {entities}")

        result = {"intent": intent}
        result.update(entities)
        return result

    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        print("\n\033[94m[MODEL EVALUATION]\033[0m")
        print(classification_report(y_test, y_pred))

    def save_model(self, filepath):
        joblib.dump(self.model, filepath)

    def load_model(self, filepath):
        self.model = joblib.load(filepath)

    def generate_training_data(self, base_prompts, names, classes):
        new_data = []
        for prompt in base_prompts:
            for name in names:
                new_data.append({
                    "prompt": prompt.replace("<name>", name),
                    "completion": json.dumps({"intent": "get_student_info", "name": name.lower()})
                })
            for cls in classes:
                new_data.append({
                    "prompt": prompt.replace("<class>", str(cls)),
                    "completion": json.dumps({"intent": "get_Students_by_class", "class": str(cls)})
                })
        return new_data
