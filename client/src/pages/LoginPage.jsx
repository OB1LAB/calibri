import React, { useEffect } from "react";
import { useContext } from "react";
import { Context } from "..";
import { Navigate } from "react-router-dom";
import Loader from "../components/Loader/Loader";
import { observer } from "mobx-react-lite";
import { INDEX_ROUTE } from "../utils/consts";

const LoginPage = () => {
  const { store } = useContext(Context);

  useEffect(() => {
    document.title = "Авторизация";
    let code = window.location.search.split("=")[1];
    if (code) {
      store.login(code);
    }
    // eslint-disable-next-line
  }, []);

  if (Object.keys(store.user).length === 0 && store.isLoading) {
    return <Loader />;
  }

  return (
    <div className="Login">
      {store.isAuth ? (
        <Navigate replace to={INDEX_ROUTE} />
      ) : (
        <h1 style={{ color: "#710000" }}>Ваш discord ID не зарегистрирован</h1>
      )}
    </div>
  );
};

export default observer(LoginPage);
