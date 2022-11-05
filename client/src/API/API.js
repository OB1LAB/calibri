import axios from "axios";

export default class API {
  static async getStaffSalaryData() {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_SERVER_URL}/getStaffSalaryData`
      );
      if (response.status !== 200) {
        return null;
      }
      return response.data;
    } catch (err) {
      console.error(err);
    }
  }
  static async getMarketItems() {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_SERVER_URL}/getMarketItems`
      );
      if (response.status !== 200) {
        return null;
      }
      return response.data;
    } catch (err) {
      console.error(err);
    }
  }
  static async login(code) {
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_SERVER_URL}/api/login`,
        {
          code: code,
        }
      );
      if (response.status !== 200) {
        return null;
      }
      return response.data;
    } catch (err) {
      console.error(err);
    }
  }
}
