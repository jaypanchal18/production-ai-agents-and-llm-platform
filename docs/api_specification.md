# API Specification Documentation

# OpenAPI Specification for FastAPI Application

openapi: 3.0.0
info:
  title: My FastAPI Application
  version: 1.0.0
  description: API documentation for the FastAPI application using TensorFlow and PostgreSQL.
servers:
  - url: http://localhost:8000
paths:
  /predict:
    post:
      summary: Predict using the TensorFlow model
      operationId: predict
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                input_data:
                  type: array
                  items:
                    type: number
              required:
                - input_data
      responses:
        '200':
          description: Successful prediction
          content:
            application/json:
              schema:
                type: object
                properties:
                  prediction:
                    type: number
        '400':
          description: Invalid input data
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
  /users:
    post:
      summary: Create a new user
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                password:
                  type: string
              required:
                - username
                - password
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  user_id:
                    type: integer
        '400':
          description: Invalid user data
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
        '409':
          description: User already exists
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
  /login:
    post:
      summary: User login
      operationId: userLogin
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                password:
                  type: string
              required:
                - username
                - password
      responses:
        '200':
          description: Successful login
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  token_type:
                    type: string
        '401':
          description: Invalid credentials
          content:
            application/json:
              schema:
                type: object
                properties:
                  detail:
                    type: string
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
security:
  - BearerAuth: []