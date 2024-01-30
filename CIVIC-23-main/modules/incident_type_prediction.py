import torch
import os
from transformers import BertTokenizerFast, AutoModelForSequenceClassification


class IncidentTypePrediction(object):

    def __init__(self):
        # Use if necessary. Model currently stored in local Google drive, bert-xxx-classification
        # self.backend = self.load_model('CD_model.pth')

        # category_map is type-confidence (String-Double) dict that stores possible types
        self.category_map = {}

        # models_used is a mapping between category and its actual pretrained model name.
        self.models_used = {}

        self.categories = ['damaged property', 'abandoned vehicles', 'aggressive driver', 'crash',
                           'drug or prostitution activity', 'lost', 'noise violation',
                           'roadway hazard', 'check welfare']

        # TODO: Fill-in the model names with the corresponding path. The names are in Google Drive.
        # Model names needs to be an extension of .h5 or .pt.
        self.model_names = ['damage_or_not.h5','abandoned_or_not.h5', 'aggressive_or_not.h5', 'crash_or_not.h5',
                            'drug_or_not.h5', 'lost_or_not.h5', 'noise_or_not.h5', 'roadway_or_not.h5',
                            'welfare_or_not.h5']

        self.barrier = 0.7

    # Hand the control to the officer.
    def handover(self, inputs):
        print(inputs)
        print("*** WARNING: sensitive word detected. Handing over to 911 ***")
        raise SystemExit

    def act(self, inputs):
        """ inputs: overall_context from main.py """
        self.map_categories()

        with open('handover_trigger_words.txt') as f:
            lines = f.readlines()
            if inputs in lines:
                self.handover(self.local_storage.context)  # handover to human

        # If confidence score passes barrier, store it in local_storage.category.
        for category in self.categories:
            conf_score = self.get_conf_score(inputs, category)
            if conf_score > self.barrier:
                self.category_map[category] = conf_score

        sorted_map = dict(sorted(self.category_map.items(), key=lambda item: item[1]))

        # returns a list of possible categories, sorted by conf_score.
        # A category is "possible" if its confidence score passes self.barrier.
        return list(sorted_map.keys())

    def map_categories(self):
        idx = 0
        for category in self.categories:
            self.models_used[category] = self.model_names[idx]
            idx += 1

    def get_conf_score(self, inputs, category):
        consistency_list = []
        num_of_trials = 20
        one = 0

        # Setting up the model
        tokenizer = BertTokenizerFast.from_pretrained(os.path.dirname(self.models_used[category]))
        model = AutoModelForSequenceClassification.from_pretrained(os.path.dirname(self.models_used[category]),
                                                                   num_labels=2)
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

    def pop(self):
        first_key = next(iter(self.category_map))
        self.category_map.pop(first_key)
        return first_key
