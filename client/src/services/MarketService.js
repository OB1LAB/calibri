import $api from "../http";

export default class MarketService {
  static fetchMarket() {
    try {
      const response = $api.get("/market");
      return response;
    } catch (err) {
      console.error(err);
    }
  }
  static buyItem(itemId, amount, selectedServer) {
    try {
      const response = $api.post("/market", {
        itemId: itemId,
        amount: amount,
        selectedServer: selectedServer,
      });
      return response;
    } catch (err) {
      console.error(err);
    }
  }
  static setTypeHistory(rowId, status) {
    try {
      const response = $api.put("/market", {
        rowId: rowId,
        status: status,
      });
      return response;
    } catch (err) {
      console.error(err);
    }
  }
}
