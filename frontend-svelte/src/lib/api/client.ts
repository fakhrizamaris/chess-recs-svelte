import { z } from 'zod';

// Schema validation - UPDATED TO MATCH PYTHON RESPONSE
export const RecommendationRequestSchema = z.object({
	user_rating: z.number().min(500).max(3000),
	favorite_openings: z.array(z.string()).min(1).max(3),
	alpha: z.number().min(0).max(1)
});

export const RecommendationResponseSchema = z.object({
	opening_name: z.string(),
	archetype: z.string().optional(),
	moves: z.string(),
	fen: z.string(), // FEN notation for board visualization
	hybrid_score: z.number(),
	cb_score: z.number(),
	cf_score: z.number(),
	win_rate_white: z.number(),
	win_rate_black: z.number(),
	win_rate_draw: z.number()
});

export type RecommendationRequest = z.infer<typeof RecommendationRequestSchema>;
export type RecommendationResponse = z.infer<typeof RecommendationResponseSchema>;

// API Client
const API_BASE = 'http://localhost:3000';

export async function getRecommendations(
	request: RecommendationRequest
): Promise<RecommendationResponse[]> {
	// Validate input
	const validated = RecommendationRequestSchema.parse(request);

	const response = await fetch(`${API_BASE}/api/recommend`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(validated)
	});

	if (!response.ok) {
		const error = await response.text();
		throw new Error(error || 'Failed to get recommendations');
	}

	const data = await response.json();
	return z.array(RecommendationResponseSchema).parse(data);
}
