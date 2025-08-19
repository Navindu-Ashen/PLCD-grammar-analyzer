#!/bin/bash

# Google Cloud Function Deployment Script
# This script deploys the parser function to Google Cloud Functions

# Configuration
FUNCTION_NAME="parse-expression"
REGION="us-central1"  # Change this to your preferred region
RUNTIME="python312"    # Python runtime version
MEMORY="512MB"        # Memory allocation
TIMEOUT="60s"         # Function timeout

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Google Cloud Function Deployment     ${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Please install Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${YELLOW}Warning: You are not authenticated with gcloud${NC}"
    echo "Please run: gcloud auth login"
    exit 1
fi

# Get current project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}Error: No project is set${NC}"
    echo "Please run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo -e "${GREEN}Current project: ${PROJECT_ID}${NC}"
echo -e "${GREEN}Function name: ${FUNCTION_NAME}${NC}"
echo -e "${GREEN}Region: ${REGION}${NC}"

# Confirm deployment
echo -e "${YELLOW}Do you want to deploy the function? (y/N)${NC}"
read -r confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Deployment cancelled${NC}"
    exit 0
fi

echo -e "${BLUE}Starting deployment...${NC}"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}Creating requirements.txt...${NC}"
    cat > requirements.txt << EOF
functions-framework==3.*
flask==2.*
ply==3.*
EOF
fi

# Deploy the function
echo -e "${BLUE}Deploying function to Google Cloud...${NC}"

gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --runtime=$RUNTIME \
    --region=$REGION \
    --source=. \
    --entry-point=parse_expression \
    --trigger-http \
    --allow-unauthenticated \
    --memory=$MEMORY \
    --timeout=$TIMEOUT \
    --set-env-vars="PYTHONPATH=." \
    --quiet

# Check deployment status
if [ $? -eq 0 ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Deployment Successful!                ${NC}"
    echo -e "${GREEN}========================================${NC}"
    
    # Get function URL
    FUNCTION_URL=$(gcloud functions describe $FUNCTION_NAME --region=$REGION --format="value(serviceConfig.uri)")
    
    echo -e "${GREEN}Function URL: ${FUNCTION_URL}${NC}"
    echo ""
    echo -e "${BLUE}Test your function with curl:${NC}"
    echo "curl -X POST ${FUNCTION_URL} \\"
    echo "  -H 'Content-Type: application/json' \\"
    echo "  -d '{\"expression\": \"int x = 5\"}'"
    echo ""
    echo -e "${BLUE}Or test with a more complex expression:${NC}"
    echo "curl -X POST ${FUNCTION_URL} \\"
    echo "  -H 'Content-Type: application/json' \\"
    echo "  -d '{\"expression\": \"double pi = 3.14 + 0.00159\"}'"
    
else
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}  Deployment Failed!                    ${NC}"
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}Please check the error messages above${NC}"
    exit 1
fi
