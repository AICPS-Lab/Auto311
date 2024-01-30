from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch
import yake
from transformers import DistilBertTokenizerFast
from case_report import CaseReport


class InformationItemization(object):

    def __init__(self):
        self.backend = torch.load('QA_model.pth')
        self.st_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.kw_extractor = yake.KeywordExtractor()
        self.tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-cased-distilled-squad')
        # self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.device = torch.device('cpu')

    def act(self, context, question, answer_sheet: CaseReport, confidence_guidance):
        field = question
        final_conf_score = None

        if question is "Auto 311, what is the location of your incident?":
            field = "incident_address"
        elif question is "What is your name?":
            field = "caller_name"
        elif question is "What is your best phone number for a call back?":
            field = "caller_phone"

        prediction = self.get_prediction(context, question)
        if confidence_guidance:
            final_conf_score = self.obtain_conf_scores(context, question)

        # Check if new answer is better and update if necessary
        answer_sheet.update_answer_sheet(field, prediction, final_conf_score)

    def obtain_conf_scores(self, context, question, num_runs=5):
        alpha = 0.2
        kw_extractor = yake.KeywordExtractor()
        embeddings = []
        keywords_list = []

        for _ in range(num_runs):
            with torch.no_grad():
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


