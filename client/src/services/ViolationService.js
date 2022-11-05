import $api from "../http";

export default class ViolationService {
  static goViolation(userId, dateStart, type, cause, selectedServer) {
    try {
      const response = $api.post("/violation", {
        userId: userId,
        dateStart: dateStart,
        type: type,
        cause: cause,
        selectedServer: selectedServer,
      });
      return response;
    } catch (err) {
      console.error(err);
    }
  }
  static deleteViolation(violationId, selectedServer) {
    try {
      const response = $api.put("/violation", {
        violationId: violationId,
        selectedServer: selectedServer,
      });
      return response;
    } catch (err) {
      console.error(err);
    }
  }
}
