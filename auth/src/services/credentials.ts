import { eq } from "drizzle-orm";
import { db } from "../core/database.js";
import { HttpError } from "../core/errors.js";
import { credentials } from "../db/schema/credentials.js";
import { hashPassword, verifyPassword } from "./password.js";
import { signAccessToken } from "./token.js";

export async function registerCredential(email: string, password: string) {
  const [existing] = await db
    .select({ id: credentials.id })
    .from(credentials)
    .where(eq(credentials.email, email))
    .limit(1);

  if (existing) {
    throw new HttpError(409, "User already exists");
  }

  const passwordHash = await hashPassword(password);
  const [created] = await db
    .insert(credentials)
    .values({ email, passwordHash })
    .returning();

  if (!created) {
    throw new HttpError(500, "Failed to create credential");
  }

  const accessToken = await signAccessToken({
    sub: created.id,
    email: created.email,
  });

  return { id: created.id, email: created.email, access_token: accessToken };
}

export async function loginCredential(email: string, password: string) {
  const [existing] = await db
    .select()
    .from(credentials)
    .where(eq(credentials.email, email))
    .limit(1);

  if (!existing) {
    throw new HttpError(401, "Invalid email or password");
  }

  const matches = await verifyPassword(existing.passwordHash, password);
  if (!matches) {
    throw new HttpError(401, "Invalid email or password");
  }

  return signAccessToken({
    sub: existing.id,
    email: existing.email,
  });
}
