#!/bin/bash

API_URL="http://localhost:8000"
UPLOAD_FILE=$1
PADDING=5
USERNAME="cool"
PASSWORD="dude"

curl -s -c cookies.txt -X POST "$API_URL/token" \
    -d "username=$USERNAME" -d "password=$PASSWORD" \
    -o /dev/null

RESPONSE=$(curl -s -b cookies.txt -X POST "$API_URL/split-vid" \
    -F "file=@$UPLOAD_FILE" \
    -F "padding=$PADDING")

echo "Response: $RESPONSE"

NUM_FILES=$(echo "$RESPONSE" | jq '.message | length')
echo "Number of files returned: $NUM_FILES"
