from modules import conversational_interface, incident_type_prediction, information_itemization, confidence_guidance
from helpers import *
import case_report

question_list_path = '../question_list.txt'

question_list = []

with open(question_list_path, 'r') as file:
    for line in file.readlines():
        question_list.append(line.strip())

conversational_interface = conversational_interface.ConversationalInterface(question_list)
incident_type_prediction = incident_type_prediction.IncidentTypePrediction()
information_itemization = information_itemization.InformationItemization()
confidence_guidance = confidence_guidance.ConfidenceGuidance()

case_report = case_report.CaseReport()

report_completed = case_report.check_complete()

overall_context = ""

turn_count = 0

incident_types_logs = []
question_asked = [] # record the previous question
routing_to_real_operator_threshold = 3

while not report_completed:
    turn_count += 1
    # find incident type

    # Agent initializes the conversation
    next_question = conversational_interface.next_question_to_ask()

    if question_asked[-1] == next_question:
        question_asked.append(next_question)

    if len(question_asked) >= routing_to_real_operator_threshold:
        sys_msg = "Routing the call to next available operator"
        conversational_interface.text_to_speech(sys_msg)
        break

    conversational_interface.text_to_speech(next_question)

    # Caller answers the question
    current_time = get_time()
    caller_cache_path = "local_cache/caller_utterance_{}.wav".format(current_time)
    caller_speaking(caller_cache_path)

    # record caller's response
    last_utterance = transcribe(caller_cache_path)
    overall_context = str(last_utterance) + overall_context

    case_report.store_interactions(utterance=last_utterance, question=next_question)

    # Predict incident type with confidence guidance
    incident_types = incident_type_prediction.act(overall_context, confidence_guidance=True)
    incident_types_logs = incident_types

    if incident_types is None:  # the incident type is not provided
        # only extract basic information
        # will not launch caller clarification by this step
        information_itemization.act(last_utterance, next_question, case_report, confidence_guidance=True)
        # updating case report if confidence score is higher
        # based on the missing required field in the outputs, e.g., {fields: [information=blank, confidence]}
        # launch user clarification by querying that field in next round of interaction

        case_report.save(turn_count)
        # case report updated with completed fields deleted
        case_report.update()
        # feed uncompleted fields to the conversational interface to determine next questions
        conversational_interface.update_question_list_from_case_report(case_report)

    else:  # the incident types are provided in a list (descending order wrt confidence)
        while incident_types is not None:
            next_incident_type_to_handle = incident_types.pop()
            # retrieve all the fields that need to be completed based on the incident type
            fields_to_collect = []
            if next_incident_type_to_handle == "minor crash report":
                protocol_path = '../phone_tree/minor_crash_report/protocol.txt'

                with open(protocol_path, 'r') as file:
                    for line in file.readlines():
                        fields_to_collect.append(line.strip())

            if next_incident_type_to_handle == "lost stolen":
                protocol_path = '../phone_tree/lost_stolen_property/protocol.txt'

                with open(protocol_path, 'r') as file:
                    for line in file.readlines():
                        fields_to_collect.append(line.strip())

            case_report.add_fields(fields_to_collect)

            # extract all information to fulfill the case report
            information_itemization.act(last_utterance, next_question, case_report, confidence_guidance=True)
            # based on the missing required field in the outputs, e.g., {fields: [information=blank, confidence]}
            # launch user clarification by querying that field in next round of interaction
            # case report updated with completed fields deleted
            case_report.save(turn_count)
            case_report.update()
            # feed uncompleted fields to the conversation interface to determine next questions
            conversational_interface.update_question_list_from_case_report(case_report)

    # 1. Obtain the most likely type(s) with highest confidence
    # 2. Modify the case report with new fields specific to the type

    # Itemize information with confidence guidance
    # 1. Obtain the most certain information with highest confidence
    # 2. Complete the case report with information
    # 3. Update interface's question list
