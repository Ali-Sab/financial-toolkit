import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("/accounts", "routes/accounts/index.tsx"),
  route("/investments", "routes/investments/index.tsx")
] satisfies RouteConfig;
