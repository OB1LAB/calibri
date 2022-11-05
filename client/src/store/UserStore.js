import { makeAutoObservable } from "mobx";
import AuthService from "../services/AuthService";
import axios from "axios";
import { API_URL } from "../http";

export default class UserStore {
  user = {};
  isAuth = false;
  isLoading = true;

  constructor() {
    makeAutoObservable(this);
  }

  setAuth(bool) {
    this.isAuth = bool;
  }

  setUser(user) {
    this.user = user;
  }

  setIsLoading(bool) {
    this.isLoading = bool;
  }

  async login(code) {
    this.setIsLoading(true);
    try {
      const response = await AuthService.login(code);
      localStorage.setItem("token", response.data.accessToken);
      this.setUser(response.data.user);
      this.setAuth(true);
    } catch (e) {
      console.log(e.response?.data?.message);
    } finally {
      this.setIsLoading(false);
    }
  }

  async logout() {
    try {
      await AuthService.logout();
      localStorage.removeItem("token");
      this.setAuth(false);
      this.setUser({});
    } catch (e) {
      console.log(e.response?.data?.message);
    }
  }

  async checkAuth() {
    try {
      const response = await axios.get(`${API_URL}/refreshToken`, {
        withCredentials: true,
      });
      localStorage.setItem("token", response.data.accessToken);
      this.setUser(response.data.user);
      this.setAuth(true);
    } catch (e) {
      console.log(e.response?.data?.message);
    } finally {
      this.setIsLoading(false);
    }
  }
}
