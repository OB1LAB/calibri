import $api from "../http";

export default class UserService {
  static fetchUsers() {
    try {
      const response = $api.get("/users");
      return response;
    } catch (err) {
      console.error(err);
    }
  }
  static addUser(name, discord_id, birthday, selectedRole, selectedServer) {
    try {
      const response = $api.post("/users", {
        name: name,
        discord_id: discord_id,
        birthday: birthday,
        selectedRole: selectedRole,
        selectedServer: selectedServer,
      });
      return response;
    } catch (err) {
      console.error(err);
    }
  }
  static editUser(
    id,
    name,
    balance,
    discord_id,
    birthday,
    selectedRole,
    selectedServer
  ) {
    try {
      const response = $api.put("/users", {
        id: id,
        name: name,
        balance: Number(balance),
        discord_id: discord_id,
        birthday: birthday,
        selectedRole: selectedRole,
        selectedServer: selectedServer,
      });
      return response;
    } catch (err) {
      console.error(err);
    }
  }
}
