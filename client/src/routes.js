import IndexPage from "./pages/IndexPage";
import StaffSalaryPage from "./pages/StaffSalaryPage";
import HistoryPage from "./pages/HistoryPage";
import MarketPage from "./pages/MarketPage";
import AdminPage from "./pages/AdminPage";
import {
  ADMIN_ROUTE,
  HISTORY_ROUTE,
  INDEX_ROUTE,
  LOGIN_ROUTE,
  MARKET_ROUTE,
  STAFF_SALARY_ROUTE,
  ACTIVITY_ROUTE,
} from "./utils/consts";
import LoginPage from "./pages/LoginPage";
import ActivityPage from "./pages/ActivityPage";

export const publicRoutes = [
  {
    path: INDEX_ROUTE,
    Element: <IndexPage />,
  },
  {
    path: LOGIN_ROUTE,
    Element: <LoginPage />,
  },
];

const JuniorSquadRoutes = [
  {
    path: HISTORY_ROUTE,
    Element: <HistoryPage />,
  },
  {
    path: STAFF_SALARY_ROUTE,
    Element: <StaffSalaryPage />,
  },
  {
    path: MARKET_ROUTE,
    Element: <MarketPage />,
  },
  {
    path: ACTIVITY_ROUTE,
    Element: <ActivityPage />,
  },
];

const AdminRoutes = [
  {
    path: HISTORY_ROUTE,
    Element: <HistoryPage />,
  },
  {
    path: MARKET_ROUTE,
    Element: <MarketPage />,
  },
  {
    path: STAFF_SALARY_ROUTE,
    Element: <StaffSalaryPage />,
  },
  {
    path: ADMIN_ROUTE,
    Element: <AdminPage />,
  },
  {
    path: ACTIVITY_ROUTE,
    Element: <ActivityPage />,
  },
];

export const authRoutes = {
  user: publicRoutes,
  helper1: JuniorSquadRoutes,
  helper2: JuniorSquadRoutes,
  mod: JuniorSquadRoutes,
  st: AdminRoutes,
  gm: AdminRoutes,
  curator: AdminRoutes,
  admin: AdminRoutes,
};
