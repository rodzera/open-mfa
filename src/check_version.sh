#!/bin/bash

RESPONSE="$1"
VERSION="$2"

echo $RESPONSE
if echo "$RESPONSE" | jq -e --arg version "$VERSION" 'select(.message != null) | .message | test("tag '\''\($version)'\'' not found")' > /dev/null; then
    echo "Tag $VERSION not found on Docker Hub. Proceeding with the build."
    exit 0
fi

if echo "$RESPONSE" | jq -e 'select(.images != null) | .images | length > 0' > /dev/null; then
    echo "Tag $VERSION exists on Docker Hub. Skipping build."
    exit 1
fi

echo "Unexpected response from Docker Hub. Skipping build."
exit 1