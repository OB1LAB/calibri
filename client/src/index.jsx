import React, { createContext } from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import UserStore from "./store/UserStore";

const store = new UserStore();
export const Context = createContext({
  store,
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <Context.Provider value={{ store }}>
      <App />
    </Context.Provider>
  </React.StrictMode>
);
