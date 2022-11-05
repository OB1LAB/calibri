import $api from "../http";

export default class SalaryService {
  static fetchSalary() {
    try {
      const response = $api.get("/salary");
      return response;
    } catch (err) {
      console.error(err);
    }
  }
  static changeCoffers(value, selectedServer) {
    try {
      const response = $api.put("/salary", {
        value: value,
        selectedServer: selectedServer,
      });
      return response;
    } catch (err) {
      console.error(err);
    }
  }
}
