// app/middleware.ts
// Next.js middleware for protecting routes that require authentication
// For client-side auth with JWT tokens, we'll focus on redirecting to login
// Actual token validation happens at the API level

import { NextRequest, NextResponse } from 'next/server';

// Define public routes that don't require authentication
const publicRoutes = ['/login', '/signup', '/', '/api/auth', '/not-found'];

export function middleware(request: NextRequest) {
  // Check if the route is public
  const isPublicRoute = publicRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  // If it's a public route, allow access
  if (isPublicRoute) {
    return NextResponse.next();
  }

  // For client-side applications using JWT tokens, we'll let the app handle
  // authentication on the client side, but we can still redirect to login
  // if needed. The actual token validation will happen when API calls are made.

  // For now, we'll allow all routes to pass through and let the client-side
  // authentication logic handle the rest
  return NextResponse.next();
}

// Define which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};