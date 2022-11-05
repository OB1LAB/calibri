import React, { useContext } from "react";
import { Context } from "../../index";
import { Routes, Route, Navigate } from "react-router-dom";
import { publicRoutes, authRoutes } from "../../routes";
import { INDEX_ROUTE } from "../../utils/consts";
import { observer } from "mobx-react-lite";

const AppRouter = observer(() => {
  const { store } = useContext(Context);
  return (
    <Routes>
      {store.isAuth &&
        authRoutes[store.user["max_role"]["name"]].map(({ path, Element }) => {
          return <Route key={path} path={path} element={Element} exact />;
        })}
      {publicRoutes.map(({ path, Element }) => (
        <Route key={path} path={path} element={Element} exact />
      ))}
      <Route path="*" element={<Navigate to={INDEX_ROUTE} />} />
    </Routes>
  );
});

export default AppRouter;
