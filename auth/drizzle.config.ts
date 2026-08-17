import { defineConfig } from "drizzle-kit";
import { env } from "./src/core/env.ts";

export default defineConfig({
  dialect: "postgresql",
  schema: "./src/db/schema/credentials.ts",
  out: "./drizzle",
  dbCredentials: {
    url: env.AUTH_DATABASE_URL,
  },
});
