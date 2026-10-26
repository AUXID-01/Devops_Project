# Stage 1: Build React Application
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

# Embed the backend URL during the Vite build process
ENV VITE_API_URL=http://localhost:8000
RUN npm run build


# Stage 2: Serve with Nginx (Non-Root)
FROM nginxinc/nginx-unprivileged:alpine

# Upgrade Alpine packages to receive security fixes
USER root
RUN apk update && apk upgrade --no-cache

# Copy the build artifacts from the previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Run Nginx as a non-root user
USER 101

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
