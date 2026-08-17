export const openApiDocument = {
  openapi: "3.1.0",
  info: {
    title: "Auth API",
    version: "0.1.0",
    description: "Credentials, JWT issue and token verification",
  },
  servers: [{ url: "/", description: "Current host" }],
  tags: [{ name: "auth" }],
  components: {
    securitySchemes: {
      bearerAuth: {
        type: "http",
        scheme: "bearer",
        bearerFormat: "JWT",
      },
    },
    schemas: {
      CredentialRequest: {
        type: "object",
        required: ["email", "password"],
        properties: {
          email: { type: "string" },
          password: { type: "string", minLength: 8 },
        },
      },
      TokenResponse: {
        type: "object",
        properties: {
          id: { type: "string", format: "uuid" },
          email: { type: "string" },
          access_token: { type: "string" },
        },
      },
      LoginResponse: {
        type: "object",
        properties: {
          access_token: { type: "string" },
        },
      },
      ErrorResponse: {
        type: "object",
        properties: {
          error: { type: "string" },
        },
      },
    },
  },
  paths: {
    "/api/v1/auth/health": {
      get: {
        tags: ["auth"],
        summary: "Health check",
        responses: {
          "200": {
            description: "Service is up",
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  properties: { status: { type: "string", example: "ok" } },
                },
              },
            },
          },
        },
      },
    },
    "/api/v1/auth/register": {
      post: {
        tags: ["auth"],
        summary: "Register credentials",
        requestBody: {
          required: true,
          content: {
            "application/json": {
              schema: { $ref: "#/components/schemas/CredentialRequest" },
            },
          },
        },
        responses: {
          "201": {
            description: "Credential created",
            content: {
              "application/json": {
                schema: { $ref: "#/components/schemas/TokenResponse" },
              },
            },
          },
          "409": {
            description: "Email already registered",
            content: {
              "application/json": {
                schema: { $ref: "#/components/schemas/ErrorResponse" },
              },
            },
          },
        },
      },
    },
    "/api/v1/auth/login": {
      post: {
        tags: ["auth"],
        summary: "Login",
        requestBody: {
          required: true,
          content: {
            "application/json": {
              schema: { $ref: "#/components/schemas/CredentialRequest" },
            },
          },
        },
        responses: {
          "200": {
            description: "JWT issued in body and httpOnly cookie",
            content: {
              "application/json": {
                schema: { $ref: "#/components/schemas/LoginResponse" },
              },
            },
          },
          "401": {
            description: "Invalid email or password",
            content: {
              "application/json": {
                schema: { $ref: "#/components/schemas/ErrorResponse" },
              },
            },
          },
        },
      },
    },
    "/api/v1/auth/verify": {
      get: {
        tags: ["auth"],
        summary: "Verify JWT",
        security: [{ bearerAuth: [] }],
        responses: {
          "200": {
            description: "Token is valid. Sets X-User-Id header.",
            headers: {
              "X-User-Id": {
                schema: { type: "string", format: "uuid" },
                description: "Authenticated user id",
              },
            },
          },
          "401": {
            description: "Missing, invalid or expired token",
          },
        },
      },
    },
  },
} as const;
