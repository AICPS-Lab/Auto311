import torch
from transformers import BertTokenizerFast, AutoModelForSequenceClassification


class CallDispatchingModule(object):

    def __init__(self):
        # Use if necessary. Model currently stored in local Google drive, bert-xxx-classification
        # self.backend = self.load_model('CD_model.pth')

        self.local_storage = {
            "context": None,
            "category": None,
            "confidence": 0,
        }

        self.categories = ['damaged property', 'abandoned vehicles', 'aggressive driver', 'animal', 'crash', 'drug or prostitution activity', 'illegal parking', 'lost', 'noise violation', 'roadway hazard', 'check welfare']
        self.barrier = 0.7

    # Hand the control to the officer.
    def handover(self, inputs):
        print(inputs)
        print("*** WARNING: sensitive word detected. Handing over to 911 ***")
        raise SystemExit

    def act(self, inputs):
        """ inputs: overall_context from main.py """


        with open('handover_trigger_words.txt') as f:
            lines = f.readlines()
            if inputs in lines:
                self.handover(self.local_storage.context)  # handover to human

        # If confidence score passes barrier, store it in local_storage.category.
        for category in self.categories:
            conf_score = self.get_conf_score(inputs, category)
            if conf_score > self.barrier:
                self.local_storage["category"].append(category)
                self.local_storage["confidence"] = conf_score

        self.local_storage["context"] = inputs
        return self.local_storage

    def get_conf_score(self, inputs, category):
        consistency_list = []
        num_of_trials = 20
        one = 0

        # FIXME: Model is currently running online HF model 'bert-base-uncased'.
        # FIXME: It should be contained in a loop that runs all 12 pre-trained models.
        # FIXME: Later on, category is used to judge which model to run from.

        # Setting up the model
        tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
        model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
        model.dropout.train()
        text = inputs
        encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')

        # Run predictions based on the pretrained model
        for _ in range(num_of_trials):
            predictions = torch.argmax(model(**encoded_input).logits)
            consistency_list.append((int(predictions.tolist())))

        # calculate the confidence score
        for element in consistency_list:
            if element == 1:
                one += 1

        result = one / len(consistency_list)
        return result

    @staticmethod
    def load_model(path):
        model = torch.load(path)
        return model
