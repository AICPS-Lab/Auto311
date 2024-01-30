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
case_report.add_incident_type("check welfare")
fields = ["incident_address","caller_name", "caller_phone"]
info = ["2525 West End", "Jack", "123-456-7899"]
case_report.fulfill_info(fields, info)


fields_to_collect = []
protocol_path = '../phone_tree/check_welfare/protocol.txt'

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

fields = ['Can you describe the people you are concerned about?', 'When did this happen?', 'What is the address of the people?', "Why do you think something might be wrong?"]
info = ["my roommates", "just now", "my next room, room 5", "they sound like fighting right now"]

case_report.fulfill_info(fields, info)

case_report.save(1)
print("Updated case report:", case_report.dictionary)

conversational_interface.update_question_list_from_case_report(case_report, incident_type)
case_report.update()
print("Next questions to ask:", conversational_interface.question_list)

print("Turn 3")

print("Question 3:", conversational_interface.next_question_to_ask())

fields = ['What is the name of the people?', "What is the people's medical history?"]
info = ["Ray", "he's been mentally ill since last July"]

case_report.fulfill_info(fields, info)

case_report.save(2)
print("Updated case report:", case_report.dictionary)

conversational_interface.update_question_list_from_case_report(case_report, incident_type)
case_report.update()
print("Next questions to ask:", conversational_interface.question_list)


print("Turn 4")

print("Question 4:", conversational_interface.next_question_to_ask())

fields = ['What is the age of the people?']
info = ["maybe 20s"]

case_report.fulfill_info(fields, info)

case_report.save(3)
print("Updated case report:", case_report.dictionary)

conversational_interface.update_question_list_from_case_report(case_report, incident_type)
case_report.update()
print("Next questions to ask:", conversational_interface.question_list)

print("Turn 5")

print("Question 5:", conversational_interface.next_question_to_ask())

fields = ['Is there obstacle for officers to access the address?']
info = ["N"]

case_report.fulfill_info(fields, info)

case_report.save(3)
print("Updated case report:", case_report.dictionary)

conversational_interface.update_question_list_from_case_report(case_report, incident_type)
case_report.update()
print("Next questions to ask:", conversational_interface.question_list)

print("Turn 6")

print("Question 6:", conversational_interface.next_question_to_ask())

fields = ['Do you request an in-person meetup with our officer?']
info = ["N"]

case_report.fulfill_info(fields, info)

case_report.save(3)
print("Updated case report:", case_report.dictionary)

conversational_interface.update_question_list_from_case_report(case_report, incident_type)
case_report.update()
print("Next questions to ask:", conversational_interface.question_list)