import $api from "../http";

export default class AuthService {
  static async login(code) {
    return $api.post("/login", { code });
  }
  static async logout() {
    return $api.post("/logout");
  }
  static async refreshToken() {
    return $api.get("/refreshToken");
  }
}
