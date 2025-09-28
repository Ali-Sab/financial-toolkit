import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("/investment-performance", "routes/investment-performance/index.tsx")
] satisfies RouteConfig;
