# filename: use_model.py
from agent.model.script import StudentInfoModel  # replace with actual filename

# Initialize
model = StudentInfoModel()

# Load trained models
model.load_model("student_info_model.pkl")  # Load intent classifier
# The spaCy model is auto-loaded in your class with: spacy.load("student_ner_model")

# Example input
test_inputs = [
    "Emma Anderson ka data dikhao",
    "Class 10 ke students ki fess pending list chahiye",
    "You are a chutiya"
]

for input_text in test_inputs:
    print(f"\nInput: {input_text}")
    print("Output:", model.predict(input_text))
