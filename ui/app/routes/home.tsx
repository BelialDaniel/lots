import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Lots Management System" },
    { name: "description", content: "Lots Management System" },
  ];
}

export default function Home() {
  return <div>Home</div>;
}
