#!/bin/bash
# better-auth-setup.sh - Script to initialize Better Auth in a project

set -e

echo "Setting up Better Auth..."

# Function to detect package manager
detect_package_manager() {
    if [ -f "yarn.lock" ]; then
        PACKAGE_MANAGER="yarn"
    elif [ -f "pnpm-lock.yaml" ]; then
        PACKAGE_MANAGER="pnpm"
    else
        PACKAGE_MANAGER="npm"
    fi
    echo "Detected package manager: $PACKAGE_MANAGER"
}

# Function to install dependencies based on framework
install_dependencies() {
    FRAMEWORK=$1
    DB_TYPE=$2

    case $FRAMEWORK in
        "nextjs")
            echo "Installing Next.js dependencies..."
            if [ "$PACKAGE_MANAGER" = "yarn" ]; then
                yarn add better-auth better-auth/next-js better-auth/react
            elif [ "$PACKAGE_MANAGER" = "pnpm" ]; then
                pnpm add better-auth better-auth/next-js better-auth/react
            else
                npm install better-auth better-auth/next-js better-auth/react
            fi
            ;;
        "express")
            echo "Installing Express dependencies..."
            if [ "$PACKAGE_MANAGER" = "yarn" ]; then
                yarn add better-auth better-auth/node
            elif [ "$PACKAGE_MANAGER" = "pnpm" ]; then
                pnpm add better-auth better-auth/node
            else
                npm install better-auth better-auth/node
            fi
            ;;
        *)
            echo "Installing base dependencies..."
            if [ "$PACKAGE_MANAGER" = "yarn" ]; then
                yarn add better-auth
            elif [ "$PACKAGE_MANAGER" = "pnpm" ]; then
                pnpm add better-auth
            else
                npm install better-auth
            fi
            ;;
    esac

    # Install database adapter if needed
    case $DB_TYPE in
        "prisma")
            if [ "$PACKAGE_MANAGER" = "yarn" ]; then
                yarn add better-auth/adapters/prisma
            elif [ "$PACKAGE_MANAGER" = "pnpm" ]; then
                pnpm add better-auth/adapters/prisma
            else
                npm install better-auth/adapters/prisma
            fi
            ;;
        "drizzle")
            if [ "$PACKAGE_MANAGER" = "yarn" ]; then
                yarn add better-auth/adapters/drizzle
            elif [ "$PACKAGE_MANAGER" = "pnpm" ]; then
                pnpm add better-auth/adapters/drizzle
            else
                npm install better-auth/adapters/drizzle
            fi
            ;;
        "mongodb")
            if [ "$PACKAGE_MANAGER" = "yarn" ]; then
                yarn add better-auth/adapters/mongodb
            elif [ "$PACKAGE_MANAGER" = "pnpm" ]; then
                pnpm add better-auth/adapters/mongodb
            else
                npm install better-auth/adapters/mongodb
            fi
            ;;
    esac

    echo "Dependencies installed successfully!"
}

# Main execution
if [ $# -lt 2 ]; then
    echo "Usage: $0 <framework> <db_type>"
    echo "Frameworks: nextjs, express"
    echo "DB Types: postgresql, mysql, sqlite, mongodb, prisma, drizzle"
    exit 1
fi

FRAMEWORK=$1
DB_TYPE=$2

detect_package_manager
install_dependencies $FRAMEWORK $DB_TYPE

echo "Better Auth setup complete!"
echo ""
echo "Next steps:"
echo "1. Create lib/auth.ts with your configuration"
echo "2. Set up environment variables in .env"
echo "3. For Next.js, create the API route handler"
echo "4. For Next.js, create client configuration"