import React from "react";
import { MARKET_ROUTE } from "../../utils/consts";
import classes from "./Information.module.css";
import { Link } from "react-router-dom";

export default function InformationExchange() {
  return (
    <div className={classes.information}>
      <div className={classes.exchange}>
        <h2>Обмен заработной платы</h2>
        <p>
          Обмену подлежит любой товар или услуга, находящийся в
          <Link to={MARKET_ROUTE}> магазине</Link>
        </p>
      </div>
    </div>
  );
}
