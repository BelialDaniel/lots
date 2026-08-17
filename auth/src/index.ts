import { sql } from "drizzle-orm";
import { createApp } from "./app.js";
import { db } from "./core/database.js";
import { env } from "./core/env.js";

await db.execute(sql`SELECT 1`);

const app = createApp();

app.listen(env.PORT, env.HOST, () => {
  console.log(`Auth service listening on ${env.HOST}:${env.PORT}`);
});
