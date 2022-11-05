import { useState } from "react";
import VacationService from "../../services/VacationService";
import Modal from "../modal/Modal";
import classes from "./Admin.module.css";

export default function Vacation({ modal, setModal, selectedServer, user }) {
  const [startDay, setStartDay] = useState(
    new Date().toLocaleDateString().split(".").reverse().join("-")
  );
  const [endDay, setEndDay] = useState(
    new Date().toLocaleDateString().split(".").reverse().join("-")
  );
  const [cause, setCause] = useState("");

  const setVacation = async () => {
    await VacationService.goVacation(
      user.id,
      startDay,
      endDay,
      cause,
      selectedServer
    );
  };

  return (
    <div className={classes.reportModal}>
      <Modal visible={modal} setVisible={setModal}>
        <div className={classes.modalContentMain}>
          <div className={classes.modalContent}>
            <h2>Начало: </h2>
            <input
              value={startDay}
              onChange={(e) => setStartDay(e.target.value)}
              type="date"
            />
          </div>
          <div className={classes.modalContent}>
            <h2>Конец: </h2>
            <input
              type="date"
              value={endDay}
              onChange={(e) => setEndDay(e.target.value)}
            />
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
              setVacation();
              setModal(false);
            }}
          >
            Отправить в отпуск
          </button>
        </div>
      </Modal>
    </div>
  );
}
