import { jwtVerify, SignJWT } from "jose";
import { env } from "../core/env.js";

const secret = new TextEncoder().encode(env.JWT_SECRET);
const algorithm = "HS256";

export type AccessTokenPayload = {
  sub: string;
  email: string;
};

export async function signAccessToken(payload: AccessTokenPayload): Promise<string> {
  return new SignJWT({ email: payload.email })
    .setProtectedHeader({ alg: algorithm })
    .setSubject(payload.sub)
    .setIssuedAt()
    .setExpirationTime(new Date(Date.now() + env.JWT_EXPIRES_IN * 60 * 1000))
    .sign(secret);
}

export async function verifyAccessToken(token: string): Promise<AccessTokenPayload> {
  const { payload } = await jwtVerify(token, secret, { algorithms: [algorithm] });
  if (typeof payload.sub !== "string" || typeof payload.email !== "string") {
    throw new Error("Invalid token payload");
  }
  return { sub: payload.sub, email: payload.email };
}
