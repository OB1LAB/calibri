import classes from "./Criteria.module.css";

export default function CriteriaViolations() {
  return (
    <table className={`${classes.criteriaTable} ${classes.violations}`}>
      <thead>
        <tr>
          <td colSpan="2" style={{ color: "red", fontWeight: "bold" }}>
            Нарушения
          </td>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Лёгкое</td>
          <td>-50</td>
        </tr>
        <tr>
          <td>Строгое</td>
          <td>-100</td>
        </tr>
        <tr>
          <td>Грубое</td>
          <td>-200</td>
        </tr>
        <tr>
          <td>Выговор</td>
          <td>Лишение З/П на месяц</td>
        </tr>
      </tbody>
    </table>
  );
}
