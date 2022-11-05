import React, { useState, useEffect, useMemo, useContext } from "react";
import SelectServer from "../components/Selectors/SelectServer";
import SelectCategories from "../components/Selectors/SelectCategories";
import ItemsList from "../components/MarketItems/ItemsList";
import Loader from "../components/Loader/Loader";
import "../styles/Market.css";
import { Context } from "..";
import SelectTypeItems from "../components/Selectors/SelectTypeItems";
import MarketService from "../services/MarketService";

export default function MarketPage() {
  let server = "";
  const { store } = useContext(Context);
  const [items, setItems] = useState({});
  const [typeItem, setTypeItem] = useState("donate");
  const [categoriesFilter, setCategoriesFilter] = useState([]);
  const [search, setSearch] = useState("");

  if (store.user["dt"]["lvl"] > 1 && store.user["tmrpg"]["lvl"] > 1) {
    server = "dt";
  } else {
    if (store.user["dt"]["lvl"] > 1) {
      server = "dt";
    } else if (store.user["tmrpg"]["lvl"] > 1) {
      server = "tmrpg";
    }
  }
  const [selectedServer, setselectedServer] = useState(server);

  useEffect(() => {
    const setMarket = async () => {
      const response = await MarketService.fetchMarket();
      response && setItems(response.data);
    };
    setMarket();
    document.title = "Магазин";
  }, []);

  const marketItems = useMemo(() => {
    if (Object.keys(items).length === 0) {
      return [];
    } else if (typeItem === "items") {
      if (categoriesFilter.length > 0) {
        let sortList = [];
        categoriesFilter.map((cat) => {
          return sortList.push(cat["value"]);
        });
        return items[selectedServer].filter((item) =>
          sortList.includes(item["cat"])
        );
      } else {
        return items[selectedServer];
      }
    }
    return items[typeItem];
  }, [categoriesFilter, items, selectedServer, typeItem]);

  const filteredAndSearchedItems = useMemo(() => {
    return marketItems.filter((item) =>
      item["viewName"].toLowerCase().includes(search.toLowerCase())
    );
  }, [search, marketItems]);

  if (Object.keys(items).length === 0) {
    return <Loader />;
  }

  return (
    <div className="market">
      <div className="selector">
        {store.user["dt"]["lvl"] > 1 && store.user["tmrpg"]["lvl"] > 1 && (
          <SelectServer
            onChange={({ value }) => {
              setCategoriesFilter([]);
              setselectedServer(value);
            }}
          />
        )}
      </div>
      <input
        className="find"
        placeholder="Поиск..."
        onChange={(e) => setSearch(e.target.value)}
      ></input>
      <SelectTypeItems itemType={typeItem} setType={setTypeItem} />
      {typeItem === "items" && (
        <div className="selector">
          <SelectCategories
            categoriesFilter={categoriesFilter}
            selectedServer={selectedServer}
            onChange={(value) => {
              setCategoriesFilter(value);
            }}
          />
        </div>
      )}
      <ItemsList
        selectedServer={selectedServer}
        user={store.user}
        items={filteredAndSearchedItems}
      />
    </div>
  );
}
