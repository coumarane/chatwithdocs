# # Stage 1: Build the Next.js app
# FROM node:18 AS builder
# WORKDIR /app

# # Copy package.json and install dependencies
# COPY package.json package-lock.json ./
# RUN npm install

# # Copy the entire project
# COPY . .

# # Ensure environment variables are available during build
# COPY .env.dev .env

# # Build the Next.js app
# RUN npm run build

# # Stage 2: Serve with Nginx
# FROM nginx:latest
# WORKDIR /usr/share/nginx/html

# # Remove default Nginx static files
# RUN rm -rf ./*

# # Copy built Next.js app from previous stage
# COPY --from=builder /app/.next /usr/share/nginx/html/.next
# COPY --from=builder /app/public /usr/share/nginx/html/public

# # Copy custom Nginx configuration
# COPY nginx.conf /etc/nginx/nginx.conf

# # Expose port
# EXPOSE 3000

# # Start Nginx
# CMD ["nginx", "-g", "daemon off;"]


FROM node:18
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the entire project and the environment file
COPY . .
COPY .env.dev .env

# Build the Next.js app
RUN npm run build

# Expose the Next.js default port
EXPOSE 3002

# Start the Next.js production server
CMD ["npm", "start"]
