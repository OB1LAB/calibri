import React, { useState } from "react";
import classes from "./Items.module.css";
import Modal from "../modal/Modal";
import MarketService from "../../services/MarketService";

const formatter = new Intl.NumberFormat("en-US", {
  minimumFractionDigits: 0,
  maximumFractionDigits: 2,
});

export default function Item({
  itemId,
  name,
  price,
  img_url,
  user,
  selectedServer,
}) {
  const [amount, setAmount] = useState(1);
  const [modal, setModal] = useState(false);

  const buyItem = async () => {
    await MarketService.buyItem(itemId, amount, selectedServer);
  };

  return (
    <div className={classes.item}>
      <p
        className={classes.name}
        dangerouslySetInnerHTML={{ __html: name.split("|")[0] }}
      />
      <img alt="" src={img_url}></img>
      {name.includes("|") ? (
        <button onClick={() => setModal(true)}>
          {price + " | " + name.split("|")[1]}
        </button>
      ) : (
        <button onClick={() => setModal(true)}>{price}</button>
      )}
      <Modal visible={modal} setVisible={setModal}>
        <div className={classes.modalContent}>
          <div className={classes.modalInfo}>
            <h3 dangerouslySetInnerHTML={{ __html: name }}></h3>
            <img alt="" src={img_url}></img>
          </div>
          <div className={classes.buy}>
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
              placeholder="Количество..."
            ></input>
            <button
              disabled={user.balance - price * amount < 0 || amount <= 0}
              onClick={() => {
                setModal(false);
                buyItem();
                user.balance -= price * amount;
              }}
            >
              Купить
            </button>
            <span>Баланс: {user.balance}</span>
            {user.balance - price * amount < -100000000 ? (
              <span>Останется: -∞</span>
            ) : (
              <span>
                Останется: {formatter.format(user.balance - price * amount)}
              </span>
            )}
          </div>
        </div>
      </Modal>
    </div>
  );
}
