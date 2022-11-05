import React from "react";
import classes from "./Items.module.css";
import Item from "./Item";

export default function ItemList({ items, user, selectedServer }) {
  return (
    <div className={classes.itemsList}>
      {items.map((marketItem) => {
        return (
          <Item
            key={marketItem["id"]}
            itemId={marketItem["id"]}
            name={marketItem["viewName"]}
            price={marketItem["price"]}
            img_url={marketItem["img_path"]}
            selectedServer={selectedServer}
            user={user}
          />
        );
      })}
    </div>
  );
}
