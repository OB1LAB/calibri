import $api from "../http";

export default class VacationService {
  static goVacation(userId, dateStart, dateEnd, cause, selectedServer) {
    try {
      const response = $api.post("/vacation", {
        userId: userId,
        dateStart: dateStart,
        dateEnd: dateEnd,
        cause: cause,
        selectedServer: selectedServer,
      });
      return response;
    } catch (err) {
      console.error(err);
    }
  }
  static deleteVacation(vacationId, selectedServer) {
    try {
      const response = $api.put("/vacation", {
        vacationId: vacationId,
        selectedServer: selectedServer,
      });
      return response;
    } catch (err) {
      console.error(err);
    }
  }
}
