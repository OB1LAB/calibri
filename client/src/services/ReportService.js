import $api from "../http";

export default class ReportService {
  static editReport(selectedServer, days) {
    try {
      const response = $api.put("/report", {
        selectedServer: selectedServer,
        days: days,
      });
      return response;
    } catch (err) {
      console.error(err);
    }
  }
}
