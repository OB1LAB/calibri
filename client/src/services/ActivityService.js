import $api from "../http";

export default class ActivityService {
  static fetchPlayers() {
    try {
      const response = $api.get("/activity");
      return response;
    } catch (err) {
      console.error(err);
    }
  }
  static fetchActivityPlayers(date1, date2, players, selectedServer) {
    try {
      const response = $api.post("/activity", {
        date1: date1,
        date2: date2,
        players: players,
        selectedServer: selectedServer,
      });
      return response;
    } catch (err) {
      console.error(err);
    }
  }
}
