import "dotenv/config";
import { z } from "zod";

function interpolate(value: string): string {
  return value.replace(/\$\{([^}]+)\}/g, (_, name: string) => {
    const resolved = process.env[name];
    if (resolved === undefined) {
      throw new Error(`Missing env var ${name} referenced in interpolation`);
    }
    return interpolate(resolved);
  });
}

const envSchema = z.object({
  AUTH_DB_NAME: z.string().min(1),
  AUTH_DATABASE_URL: z.string().min(1),
  JWT_SECRET: z.string().min(32),
  JWT_EXPIRES_IN: z.coerce.number().int().positive().default(15),
  COOKIE_NAME: z.string().min(1).default("access_token"),
  COOKIE_SECURE: z
    .enum(["true", "false"])
    .default("false")
    .transform((value) => value === "true"),
  HOST: z.string().min(1).default("0.0.0.0"),
  PORT: z.coerce.number().int().positive().default(8000),
});

const rawUrl = process.env.AUTH_DATABASE_URL;
if (rawUrl) {
  process.env.AUTH_DATABASE_URL = interpolate(rawUrl).replace(
    "postgresql+asyncpg",
    "postgresql",
  );
}

const parsed = envSchema.safeParse(process.env);
if (!parsed.success) {
  console.error("Invalid auth environment:", parsed.error.issues);
  process.exit(1);
}

export const env = parsed.data;
