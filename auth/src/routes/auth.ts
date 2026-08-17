import { Router } from "express";
import { getAccessTokenFromRequest, setAccessTokenCookie } from "../core/cookie.js";
import { HttpError } from "../core/errors.js";
import { loginBodySchema, registerBodySchema } from "../schemas/auth.js";
import { loginCredential, registerCredential } from "../services/credentials.js";
import { verifyAccessToken } from "../services/token.js";

export const authRouter = Router();

authRouter.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

authRouter.post("/register", async (req, res) => {
  const body = registerBodySchema.parse(req.body);
  const result = await registerCredential(body.email, body.password);
  res.status(201).json(result);
});

authRouter.post("/login", async (req, res) => {
  const body = loginBodySchema.parse(req.body);
  const accessToken = await loginCredential(body.email, body.password);

  setAccessTokenCookie(res, accessToken);
  res.json({ access_token: accessToken });
});

authRouter.get("/verify", async (req, res) => {
  const token = getAccessTokenFromRequest(req);
  if (!token) {
    throw new HttpError(401, "Missing bearer token");
  }

  const payload = await verifyAccessToken(token);
  res.setHeader("X-User-Id", payload.sub);
  res.status(200).end();
});
