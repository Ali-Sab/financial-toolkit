import type { Route } from "./+types/home";
import Welcome from "./welcome/welcome";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Financial Toolkit - Dashboard" },
    { name: "description", content: "Personal financial management dashboard" },
  ];
}

export default function Home() {
  return <Welcome />;
}
