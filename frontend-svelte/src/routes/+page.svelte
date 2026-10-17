<script lang="ts">
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import Logo from '$lib/components/Logo.svelte';
	import RangeField from '$lib/components/RangeField.svelte';
	import OpeningPicker from '$lib/components/OpeningPicker.svelte';
	import ResultCard from '$lib/components/ResultCard.svelte';
	import ChessBoard from '$lib/components/ChessBoard.svelte';
	import { getRecommendations, endpoints, type RecommendationResponse } from '$lib/api/client';

	const START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';

	let eloRating = 1500;
	let favoriteOpenings: string[] = [];
	let alpha = 0.5;
	let totalOpenings = 0;

	let results: RecommendationResponse[] = [];
	let isLoading = false;
	let hasSearched = false;
	let errorMessage = '';
	let serverStatus: 'checking' | 'online' | 'offline' = 'checking';

	/** Ringkasan permintaan terakhir, agar judul hasil tidak berubah saat form diutak-atik */
	let lastQuery = { rating: 0, openings: [] as string[] };

	function band(rating: number) {
		if (rating < 1000) return 'New to the game';
		if (rating < 1400) return 'Casual player';
		if (rating < 1800) return 'Club player';
		if (rating < 2200) return 'Strong club player';
		return 'Expert';
	}

	function blend(a: number) {
		const s = Math.round(a * 100);
		if (s === 50) return 'Even blend';
		return `${s}% your picks · ${100 - s}% rating peers`;
	}

	async function handleSubmit() {
		if (favoriteOpenings.length === 0) {
			toast.error('Pick at least one opening you already play.');
			return;
		}

		isLoading = true;
		hasSearched = true;
		errorMessage = '';
		results = [];
		lastQuery = { rating: eloRating, openings: [...favoriteOpenings] };

		try {
			results = await getRecommendations({
				user_rating: eloRating,
				favorite_openings: favoriteOpenings,
				alpha
			});
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'Failed to get recommendations';
			toast.error('Couldn’t get recommendations. Try again in a moment.');
			console.error(error);
		} finally {
			isLoading = false;
		}
	}

	onMount(() => {
		fetch(endpoints.health())
			.then((res) => (serverStatus = res.ok ? 'online' : 'offline'))
			.catch(() => (serverStatus = 'offline'));
	});
</script>

<svelte:head>
	<title>ChessRecs · Find the next opening you’ll actually play</title>
</svelte:head>

<div class="page">
	<header class="masthead">
		<a class="brand" href="/" aria-label="ChessRecs home">
			<Logo size={26} />
			<span class="wordmark">ChessRecs</span>
		</a>
		<nav class="nav">
			<span class="status kicker" data-status={serverStatus} aria-live="polite">
				<i aria-hidden="true"></i>
				{serverStatus === 'checking' ? 'Connecting' : serverStatus === 'online' ? 'Server online' : 'Server offline'}
			</span>
			<a href="#how">How it works</a>
			<a href="https://github.com/fakhrizamaris/chess-recs-svelte" target="_blank" rel="noopener noreferrer">Source</a>
		</nav>
	</header>

	<section class="hero rise">
		<p class="kicker">Opening recommender · Lichess data</p>
		<h1>Find the next opening you’ll actually play.</h1>
		<p class="lede">
			Tell us your rating and the openings you already enjoy. We suggest five lines that fit both,
			drawn from 20,058 rated games across {totalOpenings ? totalOpenings.toLocaleString('en-US') : '1,477'} openings.
		</p>
	</section>

	<main class="workspace">
		<form class="sheet rise" style="animation-delay: 80ms" on:submit|preventDefault={handleSubmit}>
			<div class="field">
				<div class="field-head">
					<span class="field-no">01</span>
					<label for="rating">Your rating</label>
				</div>
				<div class="readout">
					<span class="readout-value tabular">{eloRating}</span>
					<span class="readout-note">{band(eloRating)}</span>
				</div>
				<RangeField
					id="rating"
					bind:value={eloRating}
					min={500}
					max={3000}
					step={50}
					valueText="{eloRating}, {band(eloRating)}"
					startLabel="500"
					endLabel="3000"
				/>
			</div>

			<div class="field">
				<div class="field-head">
					<span class="field-no">02</span>
					<label for="opening-search">Openings you already play</label>
				</div>
				<OpeningPicker bind:selected={favoriteOpenings} bind:total={totalOpenings} maxSelections={3} />
			</div>

			<div class="field">
				<div class="field-head">
					<span class="field-no">03</span>
					<label for="alpha">What should lead</label>
				</div>
				<p class="readout-note blend tabular">{blend(alpha)}</p>
				<RangeField
					id="alpha"
					bind:value={alpha}
					min={0}
					max={1}
					step={0.1}
					valueText={blend(alpha)}
					startLabel="Players near my rating"
					endLabel="Similar to my picks"
				/>
			</div>

			<button class="submit" type="submit" disabled={isLoading || favoriteOpenings.length === 0}>
				{#if isLoading}
					<span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>
					Reading the games
				{:else}
					Find openings
					<svg width="18" height="12" viewBox="0 0 18 12" aria-hidden="true"
						><path d="M0 6h16M11 1l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.6" /></svg
					>
				{/if}
			</button>
			{#if favoriteOpenings.length === 0}
				<p class="submit-hint">Choose at least one opening to continue.</p>
			{/if}
		</form>

		<section class="results" aria-labelledby="results-title" aria-busy={isLoading}>
			<div class="results-head">
				<h2 id="results-title">Recommendations</h2>
				{#if hasSearched && !isLoading && results.length}
					<p class="kicker">
						For {lastQuery.rating} · after {lastQuery.openings.join(', ')}
					</p>
				{/if}
			</div>

			<p class="sr-only" aria-live="polite">
				{#if isLoading}Loading recommendations{:else if results.length}{results.length} recommendations ready{/if}
			</p>

			{#if isLoading}
				<ol class="skeleton" aria-hidden="true">
					{#each Array(5) as _, i}
						<li style="animation-delay: {i * 90}ms">
							<span class="sk sk-rank"></span>
							<span class="sk-lines">
								<span class="sk" style="width: 30%"></span>
								<span class="sk sk-title" style="width: {70 - i * 6}%"></span>
								<span class="sk" style="width: 45%"></span>
							</span>
						</li>
					{/each}
				</ol>
			{:else if errorMessage}
				<div class="notice">
					<p class="notice-title">The server didn’t answer.</p>
					<p>It may be waking up or briefly offline. Your choices are still here, so just try again.</p>
					<button type="button" class="link-button" on:click={handleSubmit}>Try again</button>
				</div>
			{:else if results.length > 0}
				<div class="list">
					{#each results as result, i (result.opening_name)}
						<ResultCard {result} index={i} />
					{/each}
				</div>
				<p class="list-foot">Open a line to see the position, how it scores in the dataset, and why it was picked.</p>
			{:else if hasSearched}
				<div class="notice">
					<p class="notice-title">Nothing close enough.</p>
					<p>Try a different opening, or move the slider toward players near your rating.</p>
				</div>
			{:else}
				<div class="empty">
					<div class="empty-board">
						<ChessBoard fen={START_FEN} label="Starting position" />
					</div>
					<div class="empty-text">
						<p class="empty-title">Every game starts here.</p>
						<p>
							Set your rating, add one to three openings you play, and press
							<em>Find openings</em>. Five suggestions will appear in this column.
						</p>
					</div>
				</div>
			{/if}
		</section>
	</main>

	<section id="how" class="how">
		<h2>How the recommendations work</h2>
		<ol class="how-list">
			<li>
				<span class="how-no">i.</span>
				<h3>Similar to your picks</h3>
				<p>
					Openings are compared with the ones you chose using TF-IDF similarity, so lines that
					share structure and family with your repertoire rank higher.
				</p>
			</li>
			<li>
				<span class="how-no">ii.</span>
				<h3>Played near your rating</h3>
				<p>
					A matrix-factorisation model learned what about 15,600 Lichess players actually chose.
					Players closest to your rating count the most.
				</p>
			</li>
			<li>
				<span class="how-no">iii.</span>
				<h3>Blended by you</h3>
				<p>
					The third slider sets the mix. All the way left trusts players near your rating, all the
					way right trusts similarity to your picks.
				</p>
			</li>
		</ol>
	</section>

	<footer class="footer">
		<span class="brand small"><Logo size={18} /><span>ChessRecs</span></span>
		<p>
			Data from the
			<a href="https://www.kaggle.com/datasets/datasnaek/chess" target="_blank" rel="noopener noreferrer"
				>Lichess games dataset</a
			>
			on Kaggle. Win rates reflect that sample, not all of chess.
		</p>
		<a href="https://github.com/fakhrizamaris/chess-recs-svelte" target="_blank" rel="noopener noreferrer">GitHub</a>
	</footer>
</div>

<style>
	.page {
		position: relative;
		z-index: 1;
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 clamp(1rem, 4vw, 3rem);
	}

	/* ---------- Masthead ---------- */
	.masthead {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		padding: 1.25rem 0;
		border-bottom: 1px solid var(--ink);
	}
	.brand {
		display: inline-flex;
		align-items: center;
		gap: 0.625rem;
		text-decoration: none;
		color: var(--ink);
	}
	.wordmark {
		font-family: var(--font-display);
		font-size: 1.375rem;
		letter-spacing: -0.01em;
	}
	.nav {
		display: flex;
		align-items: center;
		gap: 1.5rem;
		font-size: 0.9375rem;
	}
	.nav a {
		text-decoration: none;
		color: var(--ink-2);
	}
	.nav a:hover {
		color: var(--ink);
		text-decoration: underline;
		text-underline-offset: 4px;
	}
	.status {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
	}
	.status i {
		width: 7px;
		height: 7px;
		background: var(--rule-strong);
	}
	.status[data-status='online'] i {
		background: var(--ink);
	}
	.status[data-status='offline'] {
		color: var(--accent);
	}
	.status[data-status='offline'] i {
		background: var(--accent);
	}

	/* ---------- Hero ---------- */
	.hero {
		padding: clamp(3rem, 8vw, 6.5rem) 0 clamp(2.5rem, 6vw, 4.5rem);
		max-width: 62rem;
	}
	h1 {
		margin: 1rem 0 1.5rem;
		font-family: var(--font-display);
		font-weight: 400;
		font-size: clamp(2.5rem, 6.4vw, 5.25rem);
		line-height: 1.02;
		letter-spacing: -0.02em;
		text-wrap: balance;
	}
	.lede {
		max-width: 36rem;
		margin: 0;
		font-size: clamp(1.0625rem, 1.6vw, 1.25rem);
		line-height: 1.55;
		color: var(--ink-2);
	}

	/* ---------- Workspace ---------- */
	.workspace {
		display: grid;
		grid-template-columns: minmax(0, 400px) minmax(0, 1fr);
		gap: clamp(2rem, 5vw, 4.5rem);
		align-items: start;
		padding-bottom: 5rem;
	}

	.sheet {
		position: sticky;
		top: 1.5rem;
		display: grid;
		gap: 2rem;
		padding: 1.75rem;
		background: var(--surface);
		border: 1px solid var(--ink);
		box-shadow: 6px 6px 0 var(--ink);
	}

	.field {
		display: grid;
		gap: 0.875rem;
	}
	.field + .field {
		padding-top: 1.75rem;
		border-top: 1px solid var(--rule);
	}
	.field-head {
		display: flex;
		align-items: baseline;
		gap: 0.75rem;
	}
	.field-no {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--accent);
	}
	label {
		font-weight: 600;
		font-size: 1rem;
	}

	.readout {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: 1rem;
	}
	.readout-value {
		font-family: var(--font-mono);
		font-size: 2.75rem;
		font-weight: 500;
		line-height: 1;
		letter-spacing: -0.03em;
	}
	.readout-note {
		margin: 0;
		font-size: 0.875rem;
		color: var(--ink-2);
	}
	.blend {
		font-family: var(--font-mono);
		font-size: 0.8125rem;
	}

	.submit {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.75rem;
		width: 100%;
		padding: 1rem 1.25rem;
		background: var(--ink);
		color: var(--paper);
		border: 1px solid var(--ink);
		border-radius: var(--radius);
		font: inherit;
		font-weight: 600;
		font-size: 1rem;
		cursor: pointer;
		transition: background-color 0.15s, transform 0.15s var(--ease), box-shadow 0.15s;
	}
	.submit:hover:not(:disabled) {
		background: var(--accent);
		border-color: var(--accent);
		color: var(--on-accent);
	}
	.submit:hover:not(:disabled) svg {
		transform: translateX(3px);
	}
	.submit svg {
		transition: transform 0.2s var(--ease);
	}
	.submit:active:not(:disabled) {
		transform: translate(1px, 1px);
	}
	.submit:disabled {
		cursor: not-allowed;
		background: transparent;
		color: var(--ink-3);
		border-color: var(--rule-strong);
	}
	.submit-hint {
		margin: -1.25rem 0 0;
		font-size: 0.8125rem;
		color: var(--ink-3);
		text-align: center;
	}

	.dots {
		display: inline-flex;
		gap: 4px;
	}
	.dots i {
		width: 6px;
		height: 6px;
		background: currentColor;
		animation: blink 1s infinite;
	}
	.dots i:nth-child(2) {
		animation-delay: 0.15s;
	}
	.dots i:nth-child(3) {
		animation-delay: 0.3s;
	}
	@keyframes blink {
		0%,
		100% {
			opacity: 0.25;
		}
		50% {
			opacity: 1;
		}
	}

	/* ---------- Results ---------- */
	.results {
		min-width: 0;
	}
	.results-head {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		justify-content: space-between;
		gap: 0.5rem 1.5rem;
		padding-bottom: 1rem;
		border-bottom: 1px solid var(--ink);
	}
	h2 {
		margin: 0;
		font-family: var(--font-display);
		font-weight: 400;
		font-size: 1.75rem;
		line-height: 1.15;
	}
	.results-head .kicker {
		margin: 0;
		max-width: 100%;
		overflow-wrap: anywhere;
	}

	.list :global(.entry:first-child) {
		border-top: 0;
	}
	.list-foot {
		margin: 0;
		padding-top: 1rem;
		border-top: 1px solid var(--rule);
		font-size: 0.8125rem;
		color: var(--ink-3);
	}

	.empty {
		display: grid;
		grid-template-columns: minmax(0, 240px) 1fr;
		gap: 2rem;
		align-items: center;
		padding: 2.5rem 0;
	}
	.empty-board {
		opacity: 0.9;
	}
	.empty-title,
	.notice-title {
		margin: 0 0 0.5rem;
		font-family: var(--font-display);
		font-size: 1.5rem;
		line-height: 1.2;
		color: var(--ink);
	}
	.empty-text p:last-child,
	.notice p {
		margin: 0;
		color: var(--ink-2);
		max-width: 28rem;
	}
	.empty em {
		font-style: normal;
		font-weight: 600;
		color: var(--ink);
	}

	.notice {
		padding: 2.5rem 0;
	}
	.notice p + p {
		margin-top: 0.25rem;
	}
	.link-button {
		margin-top: 1rem;
		padding: 0;
		border: 0;
		background: none;
		font: inherit;
		font-weight: 600;
		color: var(--accent);
		text-decoration: underline;
		text-underline-offset: 4px;
		cursor: pointer;
	}

	.skeleton {
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.skeleton li {
		display: grid;
		grid-template-columns: 3.25rem 1fr;
		gap: 1.25rem;
		padding: 1.5rem 0.25rem;
		border-bottom: 1px solid var(--rule);
		animation: rise 0.4s var(--ease) both;
	}
	.sk-lines {
		display: grid;
		gap: 0.625rem;
	}
	.sk {
		display: block;
		height: 10px;
		background: var(--rule);
		animation: pulse 1.4s ease-in-out infinite;
	}
	.sk-rank {
		width: 2.25rem;
		height: 2.25rem;
	}
	.sk-title {
		height: 18px;
	}
	@keyframes pulse {
		50% {
			opacity: 0.45;
		}
	}

	/* ---------- How it works ---------- */
	.how {
		padding: 4rem 0;
		border-top: 1px solid var(--ink);
	}
	.how-list {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: clamp(1.5rem, 4vw, 3rem);
		margin: 2.5rem 0 0;
		padding: 0;
		list-style: none;
	}
	.how-list li {
		padding-top: 1rem;
		border-top: 1px solid var(--rule);
	}
	.how-no {
		font-family: var(--font-display);
		font-size: 1.25rem;
		color: var(--accent);
	}
	h3 {
		margin: 0.5rem 0;
		font-size: 1.0625rem;
		font-weight: 600;
	}
	.how-list p {
		margin: 0;
		color: var(--ink-2);
		font-size: 0.9375rem;
	}

	/* ---------- Footer ---------- */
	.footer {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 1rem 2rem;
		padding: 1.5rem 0 2.5rem;
		border-top: 1px solid var(--ink);
		font-size: 0.8125rem;
		color: var(--ink-3);
	}
	.footer p {
		margin: 0;
		flex: 1 1 22rem;
	}
	.footer a {
		color: var(--ink-2);
		text-underline-offset: 3px;
	}
	.brand.small {
		font-family: var(--font-display);
		font-size: 1rem;
	}

	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		overflow: hidden;
		clip: rect(0 0 0 0);
		white-space: nowrap;
	}

	/* ---------- Responsive ---------- */
	@media (max-width: 900px) {
		.workspace {
			grid-template-columns: 1fr;
		}
		.sheet {
			position: static;
		}
		.how-list {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 560px) {
		.nav a[href='#how'] {
			display: none;
		}
		.nav {
			gap: 1rem;
		}
		.sheet {
			padding: 1.25rem;
			box-shadow: 4px 4px 0 var(--ink);
		}
		.empty {
			grid-template-columns: 1fr;
			gap: 1.5rem;
		}
		.empty-board {
			max-width: 220px;
		}
	}
</style>
