from modules import conversational_interface
import case_report

question_list_path = '../question_list.txt'

question_list = []

with open(question_list_path, 'r') as file:
    for line in file.readlines():
        question_list.append(line.strip())

conversational_interface = conversational_interface.ConversationalInterface(question_list)
print("Initial questions to ask:", conversational_interface.queston_list)

print("Turn 1")

print("Question 1:", conversational_interface.next_question_to_ask())

case_report = case_report.CaseReport()
case_report.add_incident_type("damaged property")
fields = ["incident_address", "caller_name", "caller_phone"]
info = ["2525 West End", "Jack", "123-456-7899"]
case_report.fulfill_info(fields, info)


fields_to_collect = []
protocol_path = '../phone_tree/damaged_property/protocol.txt'

with open(protocol_path, 'r') as file:
    for line in file.readlines():
        fields_to_collect.append(line.strip())

case_report.add_fields(fields_to_collect)
incident_type = case_report.dictionary['incident type'][0]

case_report.save(0)
print("Updated case report:", case_report.dictionary)

conversational_interface.update_question_list_from_case_report(case_report, incident_type)
case_report.update()
print("Next questions to ask:", conversational_interface.queston_list)

print("Turn 2")

print("Question 2:", conversational_interface.next_question_to_ask())

fields = ['Can you describe the property?', 'Are you the property owner?', 'What is the nature of the damage?']
info = ["my car", "Y", "my car was broken in by somebody"]

case_report.fulfill_info(fields, info)

case_report.save(1)
print("Updated case report:", case_report.dictionary)

conversational_interface.update_question_list_from_case_report(case_report, incident_type)
case_report.update()
print("Next questions to ask:", conversational_interface.queston_list)

print("Turn 3")

print("Question 3:", conversational_interface.next_question_to_ask())

fields = ['When did this happen?']
info = ["last night"]

case_report.fulfill_info(fields, info)

case_report.save(2)
print("Updated case report:", case_report.dictionary)

conversational_interface.update_question_list_from_case_report(case_report, incident_type)
case_report.update()
print("Next questions to ask:", conversational_interface.queston_list)