import React, { useContext, useEffect } from "react";
import { BrowserRouter } from "react-router-dom";
import Navigation from "./components/navigations/Navigations";
import { observer } from "mobx-react-lite";
import AppRouter from "./components/navigations/AppRouter";
import "./styles/App.css";
import { Context } from ".";
import Loader from "./components/Loader/Loader";

const App = observer(() => {
  const { store } = useContext(Context);
  useEffect(() => {
    if (localStorage.getItem("token")) {
      store.checkAuth();
    } else {
      store.setIsLoading(false);
    }
    // eslint-disable-next-line
  }, []);
  if (store.isLoading) {
    return <Loader />;
  }
  return (
    <div className="mainDiv">
      <BrowserRouter>
        <Navigation />
        <AppRouter />
      </BrowserRouter>
    </div>
  );
});

export default App;
