FROM node:22 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --legacy-peer-deps

COPY . .
RUN npm run build

# Etap 2: Serwowanie plików statycznych przez Python HTTP Server
FROM python:3.12-slim

WORKDIR /app

# Skopiuj zbudowane pliki do etapu serwowania
COPY --from=builder /app/dist /app/dist

EXPOSE 5173


CMD ["python3", "-m", "http.server", "5173", "--directory", "dist"]