import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "../db/schema/index.js";
import { env } from "./env.js";

const client = postgres(env.AUTH_DATABASE_URL);
export const db = drizzle({ client, schema });
