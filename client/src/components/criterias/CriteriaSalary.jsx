import classes from "./Criteria.module.css";

export default function CriteriaSalary() {
  return (
    <table className={`${classes.criteriaTable} ${classes.solary}`}>
      <thead>
        <tr style={{ color: "darkblue", fontWeight: "bold" }}>
          <td style={{ height: "37px" }}>Должность на сервере</td>
          <td>Основная З/П</td>
          <td>Ответы на форуме</td>
          <td>Доп онлайн</td>
          <td>Доп бонус</td>
        </tr>
      </thead>
      <tbody>
        <tr style={{ width: "100px" }}>
          <td className={classes.helper1}>Стажёр</td>
          <td>50</td>
          <td>-</td>
          <td rowSpan="3">+ 0.5 за минуту онлайна после 2-ух часов</td>
          <td rowSpan="3">По решению куратора сервера</td>
        </tr>
        <tr>
          <td className={classes.helper2}>Помощник</td>
          <td>100</td>
          <td rowSpan="2">+ 15 за разобранную тему</td>
        </tr>
        <tr>
          <td className={classes.moderator}>Модератор</td>
          <td>150</td>
        </tr>
      </tbody>
    </table>
  );
}
