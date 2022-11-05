import React, { useContext } from "react";
import { Link, useLocation } from "react-router-dom";
import classes from "./Navigations.module.css";
import Logo from "../Logo.jsx";
import { Context } from "../..";
import { observer } from "mobx-react-lite";
import {
  ACTIVITY_ROUTE,
  ADMIN_ROUTE,
  HISTORY_ROUTE,
  INDEX_ROUTE,
  LOGIN_ROUTE,
  MARKET_ROUTE,
  STAFF_SALARY_ROUTE,
  viewRoutes,
} from "../../utils/consts";

const Navigation = observer(() => {
  const { store } = useContext(Context);
  const location = useLocation();
  const getColor = (path) => {
    if (path === location.pathname) {
      return classes.selected;
    }
    return classes.unSelected;
  };
  return (
    <div className={classes.navbarDiv}>
      <nav className={classes.navbar}>
        {store.isAuth &&
          viewRoutes[store.user["max_role"]["name"]].includes(
            ACTIVITY_ROUTE
          ) && (
            <Link
              to={ACTIVITY_ROUTE}
              className={`${classes.item} ${getColor(ACTIVITY_ROUTE)}`}
            >
              Игровая активность
            </Link>
          )}
        {!store.isAuth && (
          <a
            href={process.env.REACT_APP_DISCORD_LOGIN_URL}
            className={`${classes.item} ${getColor(LOGIN_ROUTE)}`}
          >
            Авторизация
          </a>
        )}
        {store.isAuth &&
          viewRoutes[store.user["max_role"]["name"]].includes(MARKET_ROUTE) && (
            <Link
              to={MARKET_ROUTE}
              className={`${classes.item} ${getColor(MARKET_ROUTE)}`}
            >
              Магазин
            </Link>
          )}
        {store.isAuth &&
          viewRoutes[store.user["max_role"]["name"]].includes(
            HISTORY_ROUTE
          ) && (
            <Link
              to={HISTORY_ROUTE}
              className={`${classes.item} ${getColor(HISTORY_ROUTE)}`}
            >
              История & Выдача
            </Link>
          )}
        <Link
          to={INDEX_ROUTE}
          className={`${classes.logo} ${getColor(INDEX_ROUTE)}`}
        >
          <Logo />
        </Link>
        {store.isAuth &&
          viewRoutes[store.user["max_role"]["name"]].includes(
            STAFF_SALARY_ROUTE
          ) && (
            <Link
              to={STAFF_SALARY_ROUTE}
              className={`${classes.item} ${getColor(STAFF_SALARY_ROUTE)}`}
            >
              Зп состава
            </Link>
          )}
        {store.isAuth &&
          viewRoutes[store.user["max_role"]["name"]].includes(ADMIN_ROUTE) && (
            <Link
              to={ADMIN_ROUTE}
              className={`${classes.item} ${getColor(ADMIN_ROUTE)}`}
            >
              Админ панель
            </Link>
          )}
        {store.isAuth && (
          <button className={classes.logout} onClick={() => store.logout()}>
            Выйти
          </button>
        )}
      </nav>
    </div>
  );
});

export default Navigation;
