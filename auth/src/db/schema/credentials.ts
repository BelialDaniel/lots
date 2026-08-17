import { pgTable, text, uuid, varchar } from "drizzle-orm/pg-core";

export const credentials = pgTable("credentials", {
  id: uuid("id").defaultRandom().primaryKey(),
  email: varchar("email", { length: 255 }).notNull().unique(),
  passwordHash: text("password_hash").notNull(),
});
