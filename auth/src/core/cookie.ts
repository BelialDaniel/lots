import type { Request, Response } from "express";
import { env } from "./env.js";

export function setAccessTokenCookie(res: Response, accessToken: string) {
  res.cookie(env.COOKIE_NAME, accessToken, {
    httpOnly: true,
    secure: env.COOKIE_SECURE,
    sameSite: "lax",
    maxAge: env.JWT_EXPIRES_IN * 60 * 1000,
    path: "/",
    ...(env.COOKIE_DOMAIN ? { domain: env.COOKIE_DOMAIN } : {}),
  });
}

export function getAccessTokenFromRequest(req: Request): string | undefined {
  const header = req.get("authorization");
  if (header?.startsWith("Bearer ")) {
    const token = header.slice("Bearer ".length).trim();
    if (token) {
      return token;
    }
  }

  return readCookie(req.get("cookie"), env.COOKIE_NAME);
}

function readCookie(header: string | undefined, name: string): string | undefined {
  if (!header) {
    return undefined;
  }

  for (const part of header.split(";")) {
    const separator = part.indexOf("=");
    if (separator === -1) {
      continue;
    }

    const key = part.slice(0, separator).trim();
    if (key === name) {
      return decodeURIComponent(part.slice(separator + 1).trim());
    }
  }

  return undefined;
}
