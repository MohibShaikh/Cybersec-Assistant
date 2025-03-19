# syntax=docker/dockerfile:1

ARG NODE_VERSION=22.14.0

FROM node:${NODE_VERSION}-alpine AS builder

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json separately for better caching
COPY package.json package-lock.json ./

# Use a cache mount to speed up dependency installation
RUN --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev

# Copy the rest of the application files
COPY . .

# Build the application
RUN npm run build


# --- Production Stage ---
FROM node:${NODE_VERSION}-alpine AS production

# Set the working directory
WORKDIR /usr/src/app

# Copy only the necessary files from the builder stage
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app/build ./build
COPY package.json ./

# Expose the port the application listens on
EXPOSE 5173

# Run the application
CMD ["npm", "run", "preview"]
