#!/bin/bash

ENV=$1
ACTION=$2

show_help() {
    echo "======================================================================="
    echo " Financial Data Warehouse - Environment Management Script"
    echo "======================================================================="
    echo "Usage: ./manage.sh [environment] [action]"
    echo ""
    echo "Environments:"
    echo "  dev   - Development environment (with bind-mounted source code)"
    echo "  test  - Test environment (for running benchmarks and tests)"
    echo "  prod  - Production environment (secured, detached mode)"
    echo ""
    echo "Actions:"
    echo "  up    - Start containers (with automatic build)"
    echo "  down  - Stop containers and remove database volumes"
    echo "  build - Force rebuild of docker images"
    echo "  logs  - View live logs"
    echo "======================================================================="
}

if [[ -z "$ENV" || -z "$ACTION" ]]; then
    show_help
    exit 1
fi

case "$ENV" in
    dev)
        COMPOSE_CMD="docker compose --env-file deploy/.env.dev -f deploy/compose.yaml -f deploy/compose.dev.yaml"
        ;;
    prod)
        COMPOSE_CMD="docker compose --env-file deploy/.env.prod -f deploy/compose.yaml -f deploy/compose.prod.yaml"
        ;;
    test)
        COMPOSE_CMD="docker compose --env-file deploy/.env.test -f deploy/compose.yaml -f deploy/compose.test.yaml"
        ;;
    *)
        echo "Error: Unknown environment '$ENV'. Choose: dev, test, or prod."
        exit 1
        ;;
esac

case "$ACTION" in
    up)
        echo "Starting [$ENV] environment..."
        if [ "$ENV" == "prod" ]; then
            $COMPOSE_CMD up -d --build
            echo "Production environment has been started in the background."
            echo "Type './manage.sh prod logs' to view the logs."
        else
            $COMPOSE_CMD up --build
        fi
        ;;
    down)
        echo "Stopping [$ENV] environment and removing volumes..."
        $COMPOSE_CMD down -v
        echo "Environment [$ENV] has been successfully cleaned up."
        ;;
    build)
        echo "Rebuilding images for [$ENV] environment..."
        $COMPOSE_CMD build
        ;;
    logs)
        $COMPOSE_CMD logs -f
        ;;
    *)
        echo "Error: Unknown action '$ACTION'. Choose: up, down, build, or logs."
        exit 1
        ;;
esac