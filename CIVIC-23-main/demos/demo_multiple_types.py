from modules import conversational_interface
import case_report

question_list_path = '../question_list.txt'

question_list = []

with open(question_list_path, 'r') as file:
    for line in file.readlines():
        question_list.append(line.strip())

conversational_interface = conversational_interface.ConversationalInterface(question_list)
print("Initial questions to ask:", conversational_interface.question_list)

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
print("Next questions to ask:", conversational_interface.question_list)

print("Turn 2")

print("Question 2:", conversational_interface.next_question_to_ask())

new_incident_type = 'lost stolen'
new_fields_to_collect = []
protocol_path = '../phone_tree/lost_stolen_property/protocol.txt'

with open(protocol_path, 'r') as file:
    for line in file.readlines():
        new_fields_to_collect.append(line.strip())

case_report.merge_between_different_types(fields_to_collect, new_fields_to_collect)
case_report.change_incident_type(new_incident_type)
conversational_interface.shift_to_new_types(case_report)

print(case_report.dictionary)

fields = ['Can you describe the property?', 'Are you the property owner?', 'When did this happen?']
info = ["my wallet", "Y", 'last night']
case_report.fulfill_info(fields, info)

case_report.save(1)
print("Updated case report:", case_report.dictionary)

conversational_interface.update_question_list_from_case_report(case_report, incident_type)
case_report.update()
print("Next questions to ask:", conversational_interface.question_list)

# fieldsA_to_collect = []
# protocol_path = 'phone_tree/damaged_property/protocol.txt'
#
# with open(protocol_path, 'r') as file:
#     for line in file.readlines():
#         fieldsA_to_collect.append(line.strip())
#
#
# fieldsB_to_collect = []
# protocol_path = 'phone_tree/lost_stolen_property/protocol.txt'
#
# with open(protocol_path, 'r') as file:
#     for line in file.readlines():
#         fieldsB_to_collect.append(line.strip())
#
# case_report = case_report.CaseReport()
# case_report.add_fields(fieldsA_to_collect)
# case_report.merge_between_different_types(fieldsA_to_collect, fieldsB_to_collect)
#
# print(case_report.dictionary)