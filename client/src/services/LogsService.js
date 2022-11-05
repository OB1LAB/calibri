import $api from "../http";

export default class LogsService {
  static fetchLogs() {
    try {
      const response = $api.get("/logs");
      return response;
    } catch (err) {
      console.error(err);
    }
  }
}
