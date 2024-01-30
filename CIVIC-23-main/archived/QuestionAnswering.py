from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch
import yake
from transformers import DistilBertTokenizerFast
import AnswerSheet


class QuestionAnsweringModule(object):
    KEY_QUESTIONS = {
        "What is your name?": ["name"],
        "What is the location of the emergency?": ["address", "where", "location"],
        "What is your phone number?": ["phone", "number"],
        "What is the suspect description?": ["suspect"],
        "What is the vehicle description?": ["vehicle", "car"],
        "What is the property description?": ["property", "item"]
    }

    def __init__(self):
        self.backend = self.load_model('QA_model.pth')
        self.st_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.kw_extractor = yake.KeywordExtractor()
        self.tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-cased-distilled-squad')
        # self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.device = torch.device('cpu')

    def act(self, inputs, answer_sheet: AnswerSheet):
        question = inputs[0]
        context = inputs[1]

        # Process the 6 key questions
        for key_question in self.KEY_QUESTIONS:
            prediction = self.get_prediction(context, key_question)
            key_inputs = [key_question, context]
            final_conf_score = self.obtain_conf_scores(key_inputs)

            # Check if new answer is better and update if necessary
            answer_sheet.update_answer_sheet(key_question, prediction, final_conf_score)

        # Process the asked question
        asked_question = self.check_key_question(question)
        if asked_question is None:  # If it's not one of the key questions
            prediction = self.get_prediction(context, question)
            final_conf_score = self.obtain_conf_scores(inputs)

            answer_sheet.update_answer_sheet(inputs[0], prediction, final_conf_score)

    def obtain_conf_scores(self, inputs, num_runs=5):
        alpha = 0.2
        kw_extractor = yake.KeywordExtractor()
        embeddings = []
        keywords_list = []

        for _ in range(num_runs):
            with torch.no_grad():
                question = inputs[0]
                context = inputs[1]
                prediction = self.get_prediction(context, question)
                print(prediction)

                # Extract keywords
                predicted_keywords = [kw[0] for kw in kw_extractor.extract_keywords(prediction)[:5]]
                keywords_list.append(predicted_keywords)

                # Compute sentence embeddings
                predicted_embedding = self.st_model.encode([prediction], convert_to_tensor=True)
                embeddings.append(predicted_embedding.cpu().numpy())

        # Compute average semantic similarity
        avg_semantic_similarity = np.mean(cosine_similarity(np.array(embeddings).squeeze()))

        # Compute keyword consistency
        common_keywords_ratios = []
        for i in range(1, num_runs):
            if keywords_list[i] and keywords_list[0]:  # if both are not empty
                common_keywords_ratio = len(set(keywords_list[i]) & set(keywords_list[0])) / max(
                    len(set(keywords_list[0])), 1)
            else:  # if either or both are empty
                common_keywords_ratio = int(keywords_list[i] == keywords_list[0])  # 1 if both are empty, else 0

            common_keywords_ratios.append(common_keywords_ratio)

        avg_common_keywords_ratio = sum(common_keywords_ratios) / num_runs

        final_conf_score = alpha * avg_common_keywords_ratio + (1 - alpha) * avg_semantic_similarity

        return final_conf_score

    def get_prediction(self, context, question):
        inputs = self.tokenizer.encode_plus(question, context, return_tensors='pt').to(self.device)
        outputs = self.backend(**inputs)

        answer_start = torch.argmax(outputs[0])
        answer_end = torch.argmax(outputs[1]) + 1

        answer = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end].cpu()))

        return answer

    def check_key_question(self, question):
        """Check if the question matches one of the key questions."""
        for key_question, keywords in self.KEY_QUESTIONS.items():
            if any(keyword in question for keyword in keywords):
                return key_question
        return None

    @staticmethod
    def load_model(path):
        model = torch.load(path)
        return model

