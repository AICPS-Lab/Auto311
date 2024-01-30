import csv
from time import gmtime, strftime


def get_time():
    return strftime("%Y-%m-%d_%H-%M-%S", gmtime())


class CaseReport():

    def __init__(self):
        self.dictionary = {
            "incident_address": {"answer": None, "confidence": 0},
            "caller_name": {"answer": None, "confidence": 0},
            "caller_phone": {"answer": None, "confidence": 0}
        }

        self.narrative_description = []
        self.auto311_questions = []

    def store_interactions(self, utterance, question):
        self.narrative_description.append(utterance)
        self.auto311_questions.append(question)

    def merge_between_different_types(self, fieldsA, fieldsB):
        # drop A, leave B
        dropped_fields = []
        for fa in fieldsA:
            if fa not in fieldsB:
                dropped_fields.append(fa)
        for df in dropped_fields:
            del self.dictionary[df]
        self.add_fields(fieldsB)

    def check_complete(self):
        for value in self.dictionary.values():
            if value == "":
                return False
        return True

    def add_incident_type(self, incident_type):
        if "incident type" in self.dictionary:
            self.dictionary['incident type'].append(incident_type)
        else:
            self.dictionary["incident type"] = [incident_type]

    def change_incident_type(self, new_type):
        self.dictionary['incident type'] = [new_type]

    def add_fields(self, fields):
        for f in fields:
            self.dictionary[f] = ""

    def fulfill_info(self, fields, information):
        for f, i in zip(fields, information):
            # assert f in self.dictionary
            self.dictionary[f] = i

    def save(self, turn_count):
        path = "turn_{}_report.csv".format(turn_count)
        w = csv.writer(open(path, "w"))

        for k,v in self.dictionary.items():
            w.writerow([k,v])

    def update(self):
        keys_to_remove = [key for key, value in self.dictionary.items() if value != ""]
        for key in keys_to_remove:
            del self.dictionary[key]

    def update_answer_sheet(self, question, answer, conf_score):
        """
        :param question: the question string
        :param answer: the answer string
        :param conf_score: the confidence score of the answer
        :return: none
        """

        if question in self.dictionary:
            if self.dictionary[question]["confidence"] is None or conf_score > self.dictionary[question]["confidence"]:
                self.dictionary[question]["answer"] = answer
                self.dictionary[question]["confidence"] = conf_score
        else:
            self.dictionary[question] = {"answer": answer, "confidence": conf_score}
