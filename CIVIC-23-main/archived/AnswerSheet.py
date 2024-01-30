import pandas as pd
import os


class AnswerSheet(object):

    def __init__(self):

        self.local_storage = {
            "QuestionAnswering": {
                "Key Questions": {
                    "What is your name?": {"answer": None, "confidence": 0},
                    "What is the location of the emergency?": {"answer": None, "confidence": 0},
                    "What is your phone number?": {"answer": None, "confidence": 0},
                    "What is the suspect description?": {"answer": None, "confidence": 0},
                    "What is the vehicle description?": {"answer": None, "confidence": 0},
                    "What is the property description?": {"answer": None, "confidence": 0}
                },
                "Other Questions": []
            },
            "CallDispatching": {
                "category": []
            }
        }


        self.default_path = os.path.join('C:', os.sep, 'Users', 'username', 'Documents', 'output.xlsx')
        self.to_file_path = self.default_path
        self.from_file_path = self.default_path

    def load_from_file(self):
        df = pd.read_excel(self.from_file_path)

        for idx, row in df.iterrows():
            question = row['question']
            answer = row['answer']
            confidence = row['confidence']

            if question in self.local_storage["QuestionAnswering"]["Key Questions"]:
                self.local_storage["QuestionAnswering"]["Key Questions"][question] = {
                    "answer": answer,
                    "confidence": confidence
                }
            else:
                self.local_storage["QuestionAnswering"]["Other Questions"].append({
                    "question": question,
                    "answer": answer,
                    "confidence": confidence
                })

    def to_file(self):
        qa_data = []

        for question, details in self.local_storage["QuestionAnswering"]["Key Questions"].items():
            qa_data.append({
                "question": question,
                "answer": details["answer"],
                "confidence": details["confidence"]
            })

        for qa in self.local_storage["QuestionAnswering"]["Other Questions"]:
            qa_data.append(qa)

        df = pd.DataFrame(qa_data)
        df.to_excel(self.to_file_path, index=False)

    def update_answer_sheet(self, question, answer, conf_score):
        """
        :param question: the question string
        :param answer: the answer string
        :param conf_score: the confidence score of the answer
        :return: none
        """

        if question in self.local_storage["QuestionAnswering"]["Key Questions"]:
            if conf_score > self.local_storage["QuestionAnswering"]["Key Questions"][question]["confidence"]:
                self.local_storage["QuestionAnswering"]["Key Questions"][question]["answer"] = answer
                self.local_storage["QuestionAnswering"]["Key Questions"][question]["confidence"] = conf_score
        else:
            # If not one of the 6 key questions
            self.local_storage["QuestionAnswering"]["Other Questions"].append({
                "question": question,
                "answer": answer,
                "confidence": conf_score
            })

    def save(self, cd_outputs):
        """
        :param cd_outputs: [context, category, confidence]
        :return: none
        """

        for cd_o in cd_outputs:
            self.local_storage["CallDispatching"].append({
                "context": cd_o[0],
                "category": cd_o[1],
                "confidence": cd_o[2]
            })

        self.to_file()
