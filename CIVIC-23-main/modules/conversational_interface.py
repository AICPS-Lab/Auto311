import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


class ConversationalInterface():

    def __init__(self, question_list):
        self.question_list = question_list
        self.additional_instructions = []

    def field_to_question(self, field):
        # load mapping
        # read mapping['field']
        q_map = {
            "incident_address": 'Auto 311, what is the location of your incident?',
            "caller_name": 'What is your name?',
            "caller_phone": 'What is your best phone number for a call back?',
        }

        return q_map[field]

    def update_question_list_from_case_report(self, case_report, incident_type):

        handover_triggered = False
        no_vehicle_related = False

        if incident_type is not None and ('Okay, tell me what is going on.' in self.question_list):
            self.question_list.remove('Okay, tell me what is going on.')

        corresponding_questions = []
        case_report_update_signal = False

        for key, value in case_report.dictionary.items():
            if value == "" and key in ["incident_address", "caller_name", "caller_phone"]:
                self.question_list.append(self.field_to_question(key))

            if value == "" and key not in ["incident_address", "caller_name",
                                           "caller_phone"] and key not in self.question_list:
                self.question_list.append(key)

            if value != "" and key in ["incident_address", "caller_name", "caller_phone"]:
                self.question_list.remove(self.field_to_question(key))

            if (incident_type == "lost stolen") and (key == "Are you the property owner?") and (value == "N"):
                self.additional_instructions.append(
                    "Please put the owner on the phone if possible, but we can still continue the call. ")
                self.question_list.remove(key)

            if (incident_type == "minor crash report") and (key == "Is the traffic being blocked?") and (
                    value == "Y"):
                self.additional_instructions.append(
                    "Please pull over your vehicles to the shoulder if possible, leave room for the traffic. ")
                self.question_list.remove(key)

            if (incident_type == "minor crash report") and (key == 'Is the vehicle still on the scene?') and (
                    value == "N"):
                corresponding_question = "Where did the vehicle go?"
                case_report_update_signal = True
                corresponding_questions.append(corresponding_question)
                self.question_list.append(corresponding_question)

            if (incident_type == "drug pros") and (key == 'Is there any vehicle involved?') and (
                    value == "N"):

                no_vehicle_related = True
                vehicle_question = 'Can you describe the vehicle with details like color, year, and make?'
                self.question_list.remove(vehicle_question)

            if (incident_type == "check welfare") and (key == 'Do you request an in-person meetup with our officer?') and (
                    value == "N"):

                no_vehicle_related = True
                vehicle_question = 'How would you describe your vehicle?'
                self.question_list.remove(vehicle_question)

            if (incident_type == "abandoned cars") and (key == "Is the vehicle occupied?") and (
                    value == "Y"):
                print("Routing the call to human operators right now...")
                self.additional_instructions.append(
                    "Routing the call to human operators right now...")
                self.question_list.remove(key)
                break

            if (incident_type == "illegal parking") and (key == "Is the vehicle occupied?") and (
                    value == "Y"):
                print("Routing the call to human operators right now...")
                self.additional_instructions.append(
                    "Routing the call to human operators right now...")
                self.question_list.remove(key)
                break

            if value != "" and key in self.question_list:
                self.question_list.remove(key)

        if case_report_update_signal:
            case_report.add_fields([q for q in corresponding_questions])

        if no_vehicle_related:
            if 'Can you describe the vehicle with details like color, year, and make?' in case_report.dictionary:
                del case_report.dictionary['Can you describe the vehicle with details like color, year, and make?']
                self.question_list.remove('Can you describe the vehicle with details like color, year, and make?')
            if "How would you describe your vehicle?" in case_report.dictionary:
                del case_report.dictionary["How would you describe your vehicle?"]
                self.question_list.remove("How would you describe your vehicle?")

    def shift_to_new_types(self, case_report):
        for q in self.question_list:
            if q not in case_report.dictionary:
                self.question_list.remove(q)

    def next_question_to_ask(self):
        instructs = ""
        for instruct in self.additional_instructions:
            instructs += str(instruct)
        self.additional_instructions = []
        return instructs + self.question_list[0]

    def text_to_speech(self, text):
        engine.say(text)
        engine.runAndWait()