import $api from "../http";

export default class HistoryService {
  static fetchHistory() {
    try {
      const response = $api.get("/history");
      return response;
    } catch (err) {
      console.error(err);
    }
  }
}
