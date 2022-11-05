import React from "react";
import Selector from "./Selector";

export const roles = [
  {
    name: "user",
    lvl: 1,
    viewName: "Пользователь",
  },
  {
    name: "helper1",
    lvl: 2,
    viewName: "Стажёр",
  },
  {
    name: "helper2",
    lvl: 3,
    viewName: "Помощник",
  },
  {
    name: "mod",
    lvl: 4,
    viewName: "Модератор",
  },
  {
    name: "st",
    lvl: 5,
    viewName: "Старший модератор",
  },
  {
    name: "gm",
    lvl: 6,
    viewName: "Главный модератор",
  },
  {
    name: "curator",
    lvl: 7,
    viewName: "Куратор",
  },
  {
    name: "admin",
    lvl: 8,
    viewName: "Разработчик",
  },
];

const actions = [
  { value: "user", label: "Пользователь" },
  { value: "helper1", label: "Стажёр" },
  { value: "helper2", label: "Помощник" },
  { value: "mod", label: "Модератор" },
  { value: "st", label: "Старший модератор" },
  { value: "gm", label: "Главный модератор" },
  { value: "curator", label: "Куратор" },
  { value: "admin", label: "Разработчик" },
];

export default function SelectRole({ value, setRole, maxLvl }) {
  return (
    <Selector
      options={actions.filter((_, index) => {
        return index < maxLvl - 1;
      })}
      value={actions[value]}
      onChange={(changeValue) => {
        setRole(actions.indexOf(changeValue) + 1);
      }}
    />
  );
}
