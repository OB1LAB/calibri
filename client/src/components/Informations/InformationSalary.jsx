import React, { useState } from "react";
import Modal from "../modal/Modal";
import classes from "./Information.module.css";
import SalaryService from "../../services/SalaryService";

export default function InformationSalary({
  value,
  user,
  selectedServer,
  setData,
}) {
  const [amount, setAmount] = useState(value);
  const [modal, setModal] = useState(false);
  const changeCoffers = async () => {
    let response = await SalaryService.changeCoffers(amount, selectedServer);
    response && setData(response.data);
  };
  return (
    <div className={classes.information}>
      <div className={classes.coffers}>
        {user[selectedServer]["lvl"] > 4 ? (
          <h2>
            Погашенный итог:{" "}
            <button
              onClick={() => {
                setAmount(value);
                setModal(true);
              }}
            >
              {value}
            </button>
          </h2>
        ) : (
          <h2>Погашенный итог: {value}</h2>
        )}
        <p>
          Значение З/П, которое было аннулировано в связи со снятием/Переводом
          модераторов
        </p>
      </div>
      <Modal visible={modal} setVisible={setModal}>
        <div className={classes.salaryModal}>
          <div className={classes.salaryCoffers}>
            <h1>Значение:</h1>
            <input
              value={amount}
              onChange={(e) => {
                if (e.target.value) {
                  setAmount(Math.ceil(e.target.value));
                } else {
                  setAmount("");
                }
              }}
              type="number"
              min="0"
            ></input>
          </div>
          <button
            onClick={() => {
              changeCoffers();
              setModal(false);
            }}
          >
            Установить
          </button>
        </div>
      </Modal>
    </div>
  );
}
