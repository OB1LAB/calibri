import React from "react";
import classes from "./Selectors.module.css";

export default function SelectTypeItems({ setType, itemType }) {
  const setValue = (value) => {
    if (value !== itemType) {
      setType(value);
    }
  };

  return (
    <div className={classes.type}>
      <button
        className={"donate" === itemType ? classes.selected : "none"}
        onClick={() => {
          setValue("donate");
        }}
      >
        Привилегии
      </button>
      <button
        className={"case" === itemType ? classes.selected : "none"}
        onClick={() => {
          setValue("case");
        }}
      >
        Кейсы
      </button>
      <button
        className={"items" === itemType ? classes.selected : "none"}
        onClick={() => {
          setValue("items");
        }}
      >
        Предметы
      </button>
    </div>
  );
}
