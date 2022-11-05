import { useState } from "react";
import classes from "./History.module.css";
import VacationService from "../../services/VacationService";
import Modal from "../modal/Modal";

export default function HistoryVacationTable({
  data,
  selectedServer,
  user,
  setData,
}) {
  const [name, setName] = useState("None");
  const [deleteId, setDeleteId] = useState(0);
  const [modal, setModal] = useState(false);
  const deleteVacation = async () => {
    const response = await VacationService.deleteVacation(
      deleteId,
      selectedServer
    );
    response && setData(response.data);
  };

  return (
    <div className={classes.access}>
      <h2>История отпусков</h2>
      <p>Во время отпуска сохраняется половина от основной ЗП</p>
      <table
        className={`${classes.generalTable} ${classes.historyVacation}`}
        id="history"
      >
        <thead>
          <tr>
            <td>Никнейм модератора</td>
            <td>Дата отпуска</td>
            <td>Дата выхода</td>
            <td>Количество дней</td>
            {user["max_role"]["lvl"] > 4 && <td>Причина</td>}
          </tr>
        </thead>
        <tbody>
          {data.map((value) => {
            return (
              <tr key={value.id}>
                {user["max_role"]["lvl"] > 4 ? (
                  <td>
                    <button
                      onClick={() => {
                        setDeleteId(value.id);
                        setName(value.user);
                        setModal(true);
                      }}
                    >
                      {value.user}
                    </button>
                  </td>
                ) : (
                  <td>{value.user}</td>
                )}
                <td>{value.start}</td>
                <td>{value.end}</td>
                <td>{value.days}</td>
                {user["max_role"]["lvl"] > 4 && <td>{value.cause}</td>}
              </tr>
            );
          })}
        </tbody>
      </table>
      <Modal visible={modal} setVisible={setModal}>
        <h1>Вы точно хотите удалить отпуск у {name}?</h1>
        <div className={classes.group}>
          <button
            onClick={() => {
              deleteVacation();
              setModal(false);
            }}
            className={classes.buttonGreen}
          >
            Да
          </button>
          <button
            onClick={() => {
              setModal(false);
            }}
            className={classes.buttonRed}
          >
            Нет
          </button>
        </div>
      </Modal>
    </div>
  );
}
