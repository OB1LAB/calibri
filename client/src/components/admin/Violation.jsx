import { useState } from "react";
import ViolationService from "../../services/ViolationService";
import UserService from "../../services/UserService";
import Modal from "../modal/Modal";
import classes from "./Admin.module.css";
import Selector from "../Selectors/Selector";

const options = [
  { value: "easy", label: "Лёгкое" },
  { value: "strict", label: "Строгое" },
  { value: "rough", label: "Грубое" },
  { value: "rebuke", label: "Выговор" },
];

export default function Violation({
  modal,
  setModal,
  selectedServer,
  user,
  setStaff,
}) {
  const [startDay, setStartDay] = useState(
    new Date().toLocaleDateString().split(".").reverse().join("-")
  );
  const [cause, setCause] = useState("");
  const [type, setType] = useState(options[0]);

  const setUsers = async () => {
    const response = await UserService.fetchUsers();
    response && setStaff(response.data);
  };

  const setViolation = async () => {
    await ViolationService.goViolation(
      user.id,
      startDay,
      type.value,
      cause,
      selectedServer
    );
    setUsers();
  };

  return (
    <div className={classes.violation}>
      <Modal visible={modal} setVisible={setModal}>
        <div className={classes.modalContentMain}>
          <div className={classes.modalContent}>
            <h2>Дата: </h2>
            <input
              value={startDay}
              onChange={(e) => setStartDay(e.target.value)}
              type="date"
            />
          </div>
          <div className={classes.modalContent}>
            <h2>Тип: </h2>
            <div className={classes.selector}>
              <Selector
                options={options}
                value={type}
                onChange={(value) => setType(value)}
              />
            </div>
          </div>
          <div className={classes.modalContent}>
            <h2>Причина: </h2>
            <input
              maxLength="256"
              value={cause}
              onChange={(e) => setCause(e.target.value)}
            />
          </div>
        </div>
        <div className={classes.modalContent}>
          <button
            onClick={() => {
              setViolation();
              setModal(false);
            }}
          >
            Выдать наказание
          </button>
        </div>
      </Modal>
    </div>
  );
}
