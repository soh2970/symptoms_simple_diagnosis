import cohere
co = cohere.Client('uSgsDraJwQGecbwJ5KTHc2GFEx2JkiIKCzK4A00s')
from cohere.responses.classify import Example


class UserData:
    def __init__(self, username, password, age, height, weight, history=None):
        self.username = username
        self.password = password  # In real applications, handle passwords securely
        self.age = age
        self.height = height
        self.weight = weight
        self.history = history if history else []
        self.co = cohere.Client('uSgsDraJwQGecbwJ5KTHc2GFEx2JkiIKCzK4A00s')

    def predict_illness(self, symptoms):
        try:
            response = self.co.classify(
                model='embed-english-v2.0',
                inputs=[symptoms],
                examples=[
                    # Examples go here; you'll need to research common illnesses and their symptoms
                    Example("fever, cough, difficulty breathing", "COVID-19"),
                    Example("loss of taste or smell, fever, cough", "COVID-19"),
                    Example("headache, nausea, sensitivity to light", "Migraine"),
                    Example("visual disturbances, vomiting, sensitivity to sounds", "Migraine"),
                    Example("sore throat, fever, swollen lymph nodes", "Strep Throat"),
                    Example("red and white patches in the throat, difficulty swallowing, fever", "Strep Throat"),
                    Example("frequent urination, excessive thirst, extreme hunger", "Diabetes"),
                    Example("unexplained weight loss, fatigue, irritability", "Diabetes"),
                    Example("abdominal pain, diarrhea, weight loss", "Crohn's Disease"),
                    Example("blood in stool, mouth sores, reduced appetite", "Crohn's Disease"),
                    Example("joint pain, stiffness, swelling", "Rheumatoid Arthritis"),
                    Example("fatigue, fever, loss of appetite", "Rheumatoid Arthritis"),
                    Example("high fever, headache, stiffness in neck", "Meningitis"),
                    Example("nausea, vomiting, confusion or difficulty concentrating", "Meningitis"),
                    Example("chest pain, shortness of breath, fatigue", "Heart Disease"),
                    Example("swelling in legs, weight gain, irregular heartbeat", "Heart Disease"),
                    Example("persistent cough, chest pain, shortness of breath", "Lung Cancer"),
                    Example("coughing up blood, hoarseness, losing weight without trying", "Lung Cancer"),
                    Example("frequent urination, pain during urination, pelvic pain", "Urinary Tract Infection"),
                    Example("blood in urine, strong-smelling urine, pelvic pain in women", "Urinary Tract Infection"),
                    Example("itchy rash, red skin, blisters", "Eczema"),
                    Example("dry, scaly skin, intense itching, red patches", "Eczema"),
                    Example("abdominal cramps, bloating, diarrhea", "Irritable Bowel Syndrome"),
                    Example("constipation, mucus in the stool, gas", "Irritable Bowel Syndrome"),
                    Example("sudden severe headache, blurred vision, difficulty speaking", "Stroke"),
                    Example("paralysis or numbness of the face, arm or leg, trouble walking", "Stroke"),
                    Example("unintended weight loss, abdominal pain, blood in stool", "Colon Cancer"),
                    Example("weakness or fatigue, change in bowel habits, unexplained weight loss", "Colon Cancer"),
                    Example("excessive sweating, difficulty sleeping, rapid heartbeat", "Hyperthyroidism"),
                    Example("weight loss, increased appetite, nervousness, anxiety", "Hyperthyroidism"),
                    Example("runny or stuffy nose, sneezing, sore throat", "Common Cold"),
                    Example("cough, mild headache, sneezing", "Common Cold"),
                    Example("red eyes, blurred vision, eye pain", "Conjunctivitis"),
                    Example("itchiness in the eyes, increased tearing, discharge from the eyes", "Conjunctivitis"),
                    Example("memory loss, difficulty performing familiar tasks, mood swings", "Alzheimer's Disease"),
                    Example("confusion with time or place, trouble understanding visual images, new problems with words in speaking or writing", "Alzheimer's Disease"),
                    Example("extreme fatigue, muscle or joint pain, sore throat", "Chronic Fatigue Syndrome"),
                    Example("unrefreshing sleep, headaches, concentration or memory problems", "Chronic Fatigue Syndrome")

                ]
            )
            # Extract the label confidence pairs
            predictions = []
            for classification in response.classifications:
                for label, label_prediction in classification.labels.items():
                    predictions.append((label, label_prediction.confidence))

            # Sort the predictions by confidence in descending order
            sorted_predictions = sorted(predictions, key=lambda x: x[1], reverse=True)

            # Take the top 3 predictions and convert confidences to percentages
            top_three_predictions = [(pred[0], pred[1]) for pred in sorted_predictions[:3]]

            return top_three_predictions
        except Exception as e:
            print(f"Error processing prediction: {e}")
            return []
