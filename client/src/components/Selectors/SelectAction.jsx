import React from "react";
import Selector from "./Selector";

const actions = [
  { value: "appointment", label: "Назначения" },
  { value: "logs", label: "Логи" },
  { value: "reportEdit", label: "Изменить последний отчёт" },
];

export default function SelectAction({ onChange }) {
  return (
    <Selector
      options={actions}
      defaultValue={actions[0]}
      onChange={({ value }) => onChange(value)}
    />
  );
}
