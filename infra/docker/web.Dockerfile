FROM node:20-alpine AS base

FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
RUN corepack enable pnpm

COPY apps/web/package.json ./apps/web/
# If there's a workspace root package.json or pnpm-workspace.yaml, copy it here
# But we only have apps/web
RUN cd apps/web && pnpm install

FROM base AS builder
WORKDIR /app
RUN corepack enable pnpm

COPY --from=deps /app/apps/web/node_modules ./apps/web/node_modules
COPY apps/web ./apps/web

ENV NEXT_TELEMETRY_DISABLED 1

WORKDIR /app/apps/web
RUN pnpm build

FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/apps/web/public ./apps/web/public

RUN mkdir -p apps/web/.next
RUN chown -R nextjs:nodejs apps/web/.next

COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/static ./apps/web/.next/static

USER nextjs

EXPOSE 3000
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Note: nextjs standalone outputs a server.js file at the root of the standalone folder (or within apps/web depending on setup)
# Usually for standalone, we run node apps/web/server.js
CMD ["node", "apps/web/server.js"]
