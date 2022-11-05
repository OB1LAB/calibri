import { useState } from "react";
import classes from "./History.module.css";
import Selector from "../Selectors/Selector";
import Modal from "../modal/Modal";
import MarketService from "../../services/MarketService";

const options = [
  { value: "На рассмотрении", label: "На рассмотрении" },
  { value: "Выдано", label: "Выдано" },
  { value: "Отказано", label: "Отказано" },
];

export default function HistoryBuyTable({ data, user, setData }) {
  const [rowId, setRowId] = useState(0);
  const [state, setState] = useState("");
  const [modal, setModal] = useState(false);
  const editStatus = async () => {
    const response = await MarketService.setTypeHistory(rowId, state);
    response && setData(response.data);
  };
  return (
    <div>
      <h2>История покупок</h2>
      <p>История покупок не очищается</p>
      <table
        className={`${classes.generalTable} ${classes.historyBuy}`}
        id="history"
      >
        <thead>
          <tr>
            <td># п/п</td>
            <td>Никнейм модератора</td>
            <td>Дата покупки</td>
            <td>Наименование услуги</td>
            <td>Количество</td>
            <td>Цена</td>
            {user["max_role"]["lvl"] > 4 && <td>Действие</td>}
          </tr>
        </thead>
        <tbody>
          {data
            .sort((a, b) => a.id - b.id)
            .map((value, index) => {
              return (
                <tr key={value.id}>
                  <td>{index + 1}</td>
                  <td>{value.user}</td>
                  <td>{value.date}</td>
                  <td dangerouslySetInnerHTML={{ __html: value.item }}></td>
                  <td>{value.amount}</td>
                  <td>{value.price}</td>
                  {user["max_role"]["lvl"] > 4 && (
                    <td>
                      <div className={classes.buySelectState}>
                        <button
                          onClick={() => {
                            setRowId(value.id);
                            setState(value.state);
                            setModal(true);
                          }}
                        >
                          {value.state}
                        </button>
                      </div>
                    </td>
                  )}
                </tr>
              );
            })}
        </tbody>
      </table>
      <Modal visible={modal} setVisible={setModal}>
        <div className={classes.historyBuyModal}>
          <Selector
            options={options}
            value={{ value: state, label: state }}
            onChange={({ value }) => setState(value)}
          />
          <button
            onClick={() => {
              editStatus();
              setModal(false);
            }}
          >
            Сохранить
          </button>
        </div>
      </Modal>
    </div>
  );
}
