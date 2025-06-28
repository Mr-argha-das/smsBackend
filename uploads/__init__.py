# {
#                                           final currentDate = DateTime.now();
#                                           final userid = box.get('id');
#                                           final date = box.get("postdate");
#                                           if (date != null &&
#                                               date !=
#                                                   "${currentDate.day}/${currentDate.month}/${currentDate.year}") {
#                                             try {
#                                               final state = APIService(
#                                                 createDio(),
#                                               );
#                                               final response = await state
#                                                   .boostPost(
#                                                     userid: userid.toString(),
#                                                     planId: planid.toString(),
#                                                     productId:
#                                                         listing
#                                                             .data
#                                                             .sellList[index]
#                                                             .id
#                                                             .toString(),
#                                                   );
#                                               if (response
#                                                       .response
#                                                       .data["status"] ==
#                                                   true) {
#                                                 await box.put(
#                                                   "postdate",
#                                                   "${currentDate.day}/${currentDate.month}/${currentDate.year}",
#                                                 );
#                                                 Fluttertoast.showToast(
#                                                   msg: "Boost succes fully",
#                                                 );
#                                               } else {
#                                                 Fluttertoast.showToast(
#                                                   msg:
#                                                       response
#                                                           .response
#                                                           .data["message"]
#                                                           .toString(),
#                                                 );
#                                               }
#                                             } catch (e) {
#                                               Fluttertoast.showToast(
#                                                 msg: "No active plan found.",
#                                               );
#                                             }
#                                           }else if (date == null) {
#                                             try {
#                                               final state = APIService(
#                                                 createDio(),
#                                               );
#                                               final response = await state
#                                                   .boostPost(
#                                                     userid: userid.toString(),
#                                                     planId: planid.toString(),
#                                                     productId:
#                                                         listing
#                                                             .data
#                                                             .sellList[index]
#                                                             .id
#                                                             .toString(),
#                                                   );
#                                               if (response
#                                                       .response
#                                                       .data["status"] ==
#                                                   true) {
#                                                 await box.put(
#                                                   "postdate",
#                                                   "${currentDate.day}/${currentDate.month}/${currentDate.year}",
#                                                 );
#                                                 Fluttertoast.showToast(
#                                                   msg: "Boost succes fully",
#                                                 );
#                                               } else {
#                                                 Fluttertoast.showToast(
#                                                   msg:
#                                                       response
#                                                           .response
#                                                           .data["message"]
#                                                           .toString(),
#                                                 );
#                                               }
#                                             } catch (e) {
#                                               Fluttertoast.showToast(
#                                                 msg: "No active plan found.",
#                                               );
#                                             }
#                                           }else{
#                                             Fluttertoast.showToast(msg: "Today post limit reache");
#                                           }
                                          
#                                         }