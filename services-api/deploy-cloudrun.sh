#!/bin/bash

# Google Cloud Run Deployment Script
# This script builds and deploys your AI service to Google Cloud Run

set -e  # Exit on error

# Configuration
PROJECT_ID="your-gcp-project-id"  # CHANGE THIS!
SERVICE_NAME="chessrecs-ai"
REGION="asia-southeast1"  # Singapore (closest to you)
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  ChessRecs AI - Cloud Run Deploy  ${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# Step 1: Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${YELLOW}Google Cloud SDK not found!${NC}"
    echo "Please install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo -e "${GREEN}✓ Google Cloud SDK found${NC}"

# Step 2: Set project
echo -e "\n${BLUE}Setting GCP project...${NC}"
gcloud config set project ${PROJECT_ID}

# Step 3: Enable required APIs
echo -e "\n${BLUE}Enabling required APIs...${NC}"
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com

echo -e "${GREEN}✓ APIs enabled${NC}"

# Step 4: Build container image
echo -e "\n${BLUE}Building container image...${NC}"
echo "This may take 5-10 minutes..."

gcloud builds submit \
    --tag ${IMAGE_NAME} \
    --timeout=20m

echo -e "${GREEN}✓ Image built successfully${NC}"

# Step 5: Deploy to Cloud Run
echo -e "\n${BLUE}Deploying to Cloud Run...${NC}"

gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 0 \
    --set-env-vars "ENVIRONMENT=production,LOG_LEVEL=info" \
    --port 8080

echo -e "${GREEN}✓ Deployment complete!${NC}"

# Step 6: Get service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --format 'value(status.url)')

echo ""
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}  Deployment Successful! 🎉${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""
echo -e "Service URL: ${BLUE}${SERVICE_URL}${NC}"
echo ""
echo "Test endpoints:"
echo -e "  Health: ${BLUE}${SERVICE_URL}/health${NC}"
echo -e "  Openings: ${BLUE}${SERVICE_URL}/openings${NC}"
echo -e "  Predict: ${BLUE}${SERVICE_URL}/predict${NC}"
echo ""
echo "Update your frontend API_BASE to:"
echo -e "  ${YELLOW}${SERVICE_URL}${NC}"
echo ""
