# ============================================
# ChessRecs NextGen - Frontend (SvelteKit)
# Multi-stage Dockerfile for production
# ============================================

# Stage 1: Build
FROM node:20-slim as builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build arguments for environment variables
ARG PUBLIC_API_GATEWAY_URL
ARG PUBLIC_AI_SERVICE_URL

# Set environment variables for build
ENV PUBLIC_API_GATEWAY_URL=$PUBLIC_API_GATEWAY_URL
ENV PUBLIC_AI_SERVICE_URL=$PUBLIC_AI_SERVICE_URL

# Build the application
RUN npm run build

# Stage 2: Production runtime
FROM node:20-slim as production

WORKDIR /app

# Copy built application
COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./

# Install only production dependencies
RUN npm install --omit=dev

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Environment variables
ENV NODE_ENV=production
ENV PORT=5173

# Expose port
EXPOSE 5173

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ || exit 1

# Run the application
CMD ["node", "build"]
