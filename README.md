# RadicaliTest

provide the equipment which are not available
Send GET request on below API
http:/localhost:2222/issuedManager


list the equipment which are in pending state
Send GET request on below API
http:/localhost:2222/isseuEquipment?id=MENTION_ID


Returns available equipment 
Send GET request on below API
http:/localhost:2222/getEquipment

Creates Equipment send the dictionary data in body raw using Postman
Send POST requets on below API
{
"id":1,
"equipment_name":"XXX",
"status":"NA/Available",
"current_owner":"XYZ"
}
in creation equipment would be only in pending state
http:/localhost:2222/getEquipment


Send GET request on below api
http:/localhost:2222/getSpecificEquipmentIssueEquipment?id=MENTION_ID



Return of the Eqipment 
Send POST request on below api
{
"id":1"
}
http:/localhost:2222/getSpecificEquipmentIssueEquipment




