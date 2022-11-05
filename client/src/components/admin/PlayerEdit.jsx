import UserService from "../../services/UserService";
import Modal from "../modal/Modal";
import SelectRole, { roles } from "../Selectors/SelectRole";
import classes from "./Admin.module.css";

export default function PlayerEdit({
  playerData,
  user,
  selectedServer,
  name,
  setName,
  discord,
  setDiscord,
  role,
  setRole,
  balance,
  setBalance,
  birthday,
  setBirthday,
  modal,
  setModal,
  setResponseModal,
  setResponseData,
  setStaff,
}) {
  const getUsers = async () => {
    const response = await UserService.fetchUsers();
    response && setStaff(response.data);
  };

  const editUser = async () => {
    try {
      await UserService.editUser(
        playerData.id,
        name,
        balance,
        discord,
        birthday,
        roles[role - 1].name,
        selectedServer
      );
      getUsers();
    } catch (err) {
      setResponseModal(true);
      let response = err.response.data.message;
      let keys = Object.keys(response);
      if (keys) {
        setResponseData({
          color: "red",
          content: `${keys[0]} ${response[keys[0]]}`,
        });
      }
    }
  };

  return (
    <div>
      <Modal visible={modal} setVisible={setModal}>
        <div className={classes.modalContentMain}>
          <div className={classes.modalContent}>
            <h2>Ник: </h2>
            <input
              maxLength="16"
              value={name}
              onChange={(e) => {
                setName(e.target.value);
              }}
            ></input>
          </div>

          <div className={classes.modalContent}>
            <h2>Дс ID: </h2>
            <input
              maxLength="20"
              value={discord}
              onChange={(e) => {
                setDiscord(e.target.value);
              }}
            ></input>
          </div>

          <div className={classes.modalContent}>
            <h2>Роль: </h2>
            <div className={classes.selector}>
              <SelectRole
                value={role - 1}
                setRole={setRole}
                maxLvl={user["max_role"]["lvl"]}
              />
            </div>
          </div>

          <div className={classes.modalContent}>
            <h2>Баланс: </h2>
            <input
              type="number"
              value={balance}
              onChange={(e) => {
                setBalance(e.target.value);
              }}
            ></input>
          </div>

          <div className={classes.modalContent}>
            <h2>Д/р: </h2>
            <input
              value={birthday}
              maxLength="32"
              onChange={(e) => setBirthday(e.target.value)}
            ></input>
          </div>
        </div>

        <div className={classes.modalContent}>
          <button
            onClick={() => {
              setModal(false);
              editUser();
            }}
          >
            Сохранить
          </button>
        </div>
      </Modal>
    </div>
  );
}
