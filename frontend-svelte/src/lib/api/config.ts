/**
 * Centralized Configuration
 *
 * All environment-dependent configurations are managed here.
 * Uses SvelteKit's PUBLIC_ prefix for client-side env vars.
 */

import { PUBLIC_API_GATEWAY_URL, PUBLIC_AI_SERVICE_URL } from '$env/static/public';

export const config = {
	/**
	 * API Gateway URL (Rust Backend)
	 * Handles: /api/recommend, /health
	 */
	apiGatewayUrl: PUBLIC_API_GATEWAY_URL || 'http://localhost:3000',

	/**
	 * AI Service URL (Python FastAPI)
	 * Handles: /openings, /predict
	 */
	aiServiceUrl: PUBLIC_AI_SERVICE_URL || 'http://localhost:8001',

	/**
	 * App Metadata
	 */
	app: {
		name: 'ChessRecs NextGen',
		version: '1.0.0',
		description: 'Smart chess opening recommendations'
	}
} as const;

// Helper functions for common endpoints
export const endpoints = {
	// API Gateway endpoints
	health: () => `${config.apiGatewayUrl}/health`,
	recommend: () => `${config.apiGatewayUrl}/api/recommend`,

	// AI Service endpoints
	openings: () => `${config.aiServiceUrl}/openings`,
	predict: () => `${config.aiServiceUrl}/predict`
} as const;
