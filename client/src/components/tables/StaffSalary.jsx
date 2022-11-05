import React from "react";
import classes from "./StaffSalary.module.css";
import ChartStaff from "../charts/ChartStaff";
import ChartActivity from "../charts/ChartActivity";
import InformationSalary from "../Informations/InformationSalary";
import InformationExchange from "../Informations/InformationExchange";

export default function StaffSalary({
  staffData,
  user,
  selectedServer,
  setData,
}) {
  return (
    <div>
      <table className={classes.staffSalaryTable} id="history">
        <thead>
          <tr>
            <td>Никнейм модератора</td>
            <td>Должность на сервере</td>
            <td>Основная зарплата</td>
            <td>Ответы на форуме</td>
            <td>Отыгранный онлайн</td>
            <td>Дополнительный онлайн</td>
            <td>Бонус</td>
            <td>Итог за неделю</td>
            <td>Общий итог</td>
            <td>День рождения</td>
          </tr>
        </thead>
        <tbody>
          {staffData["salaryPlayers"].map((player) => {
            let colorRank = classes.player;
            if (player["rank"] === "Модератор") {
              colorRank = classes.moderator;
            } else if (player["rank"] === "Помощник") {
              colorRank = classes.helper2;
            } else {
              colorRank = classes.helper1;
            }
            return (
              <tr key={player["name"]}>
                <td>{player["name"]}</td>
                <td className={colorRank}>{player["rank"]}</td>
                <td>{player["mainSalary"]}</td>
                <td>{player["answerForum"]}</td>
                <td>{player["online"]}</td>
                <td>{player["additionallyOnline"]}</td>
                <td>{player["bonus"]}</td>
                <td>{player["totalWeek"]}</td>
                <td>{player["totalAllTime"]}</td>
                <td>{player["birthday"]}</td>
              </tr>
            );
          })}
        </tbody>
        <tfoot>
          <tr>
            <td>Итог</td>
            <td>-</td>
            <td>{staffData["salaryData"]["mainSalary"]}</td>
            <td>{staffData["salaryData"]["answerForum"]}</td>
            <td>{staffData["salaryData"]["online"]}</td>
            <td>{staffData["salaryData"]["additionallyOnline"]}</td>
            <td>{staffData["salaryData"]["bonus"]}</td>
            <td>{staffData["salaryData"]["totalWeek"]}</td>
            <td>{staffData["salaryData"]["totalAllTime"]}</td>
            <td>-</td>
          </tr>
        </tfoot>
      </table>
      <div className={classes.information}>
        <InformationSalary
          user={user}
          selectedServer={selectedServer}
          value={staffData["coffers"]}
          setData={setData}
        />
        <InformationExchange />
      </div>
      <ChartStaff data={staffData["chartData"]} />
      <ChartActivity data={staffData["chartOnlineData"]} />
    </div>
  );
}
