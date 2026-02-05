# Framework Integration Guide

## Next.js Integration

### Server Configuration (lib/auth.ts)
```typescript
import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";

export const auth = betterAuth({
  // ...your config
  plugins: [
    nextCookies() // Enable cookies in server actions
  ]
});
```

### API Route Handler (app/api/auth/[...all]/route.ts)
```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

### Client Configuration (lib/auth-client.ts)
```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000",
});
```

### Middleware (middleware.ts)
```typescript
import { NextRequest, NextResponse } from "next/server";
import { getSessionCookie } from "better-auth/cookies";

export function middleware(request: NextRequest) {
  const sessionCookie = getSessionCookie(request);

  if (!sessionCookie && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/settings/:path*"]
};
```

### Protected Server Component (app/dashboard/page.tsx)
```typescript
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session) {
    redirect("/login");
  }

  return <h1>Welcome, {session.user.name}!</h1>;
}
```

### Server Action with Auth
```typescript
async function updateProfile(formData: FormData) {
  "use server";

  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session) {
    throw new Error("Unauthorized");
  }

  await auth.api.updateUser({
    body: {
      name: formData.get("name") as string
    },
    headers: await headers()
  });
}
```

## Express.js Integration

### Mounting Handler
```typescript
import express from "express";
import { toNodeHandler } from "better-auth/node";
import { auth } from "./auth";

const app = express();
const port = 3005;

app.all("/api/auth/*", toNodeHandler(auth));

// Mount express json middleware after Better Auth handler
app.use(express.json());

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```

## React Client Integration

### Sign-in Component
```typescript
"use client";

import { Button } from "@/components/ui/button";
import { authClient } from "@/lib/auth-client";

const SignInPage = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <Button
        onClick={async () => {
          await authClient.signIn.social({
            provider: "github",
            callbackURL: "/dashboard",
          });
        }}
      >
        Sign in with GitHub
      </Button>
    </div>
  );
};

export default SignInPage;
```

### Protected Client Component
```typescript
"use client";

import { authClient } from "@/lib/auth-client";
import { redirect } from "next/navigation";

const DashboardPage = () => {
  const { data, error, isPending } = authClient.useSession();

  if (isPending) {
    return <div>Loading...</div>;
  }
  if (!data || error) {
    redirect("/sign-in");
  }

  return (
    <div>
      <h1>Welcome {data.user.name}</h1>
    </div>
  );
};

export default DashboardPage;
```

## Security Considerations per Framework

### Next.js Security
- Always use `nextCookies()` plugin for server actions
- Protect server components with session checks
- Use Next.js redirects instead of client-side navigation for auth failures
- Validate headers in server actions

### Express.js Security
- Place Better Auth handler before other middleware
- Don't place `express.json()` before Better Auth handler
- Implement proper CORS policies
- Use helmet.js for additional security headers