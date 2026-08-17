import { apiReference } from "@scalar/express-api-reference";
import express from "express";
import type { ErrorRequestHandler } from "express";
import { errors as joseErrors } from "jose";
import { ZodError } from "zod";
import { HttpError } from "./core/errors.js";
import { openApiDocument } from "./openapi.js";
import { authRouter } from "./routes/auth.js";

const errorHandler: ErrorRequestHandler = (err, _req, res, _next) => {
  if (err instanceof HttpError) {
    res.status(err.statusCode).json({ error: err.message });
    return;
  }

  if (err instanceof ZodError) {
    res.status(400).json({ error: "Invalid request body", details: err.issues });
    return;
  }

  if (err instanceof joseErrors.JOSEError) {
    res.status(401).json({ error: "Invalid or expired token" });
    return;
  }

  console.error(err);
  res.status(500).json({ error: "Internal server error" });
};

export function createApp() {
  const app = express();
  app.use(express.json());
  app.get("/api/v1/auth/openapi.json", (_req, res) => {
    res.json(openApiDocument);
  });
  app.use(
    "/api/v1/auth/docs",
    apiReference({
      theme: "default",
      content: openApiDocument,
    }),
  );
  app.use("/api/v1/auth", authRouter);
  app.use(errorHandler);
  return app;
}
