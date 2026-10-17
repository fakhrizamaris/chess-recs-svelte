<script lang="ts">
	import { slide } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import type { RecommendationResponse } from '$lib/api/client';
	import ChessBoard from './ChessBoard.svelte';

	export let result: RecommendationResponse;
	export let index: number;

	let isExpanded = false;

	const pct = (v: number) => Math.round(v * 100);

	/** "Sicilian Defense: Old Sicilian" -> keluarga + varian */
	function splitName(name: string) {
		const at = name.indexOf(':');
		const clean = (s: string) => s.replace(/\s*\|\s*/g, ' · ').trim();
		if (at === -1) return { family: '', line: clean(name) };
		return { family: clean(name.slice(0, at)), line: clean(name.slice(at + 1)) };
	}

	/** "e4 c5 Nf3 Nf6" -> "1.e4 c5 2.Nf3 Nf6" */
	function numbered(moves: string) {
		const list = moves.split(/\s+/).filter((m) => m && !/^\d+\.+$/.test(m));
		const out: { n: number | null; san: string }[] = [];
		list.forEach((san, i) => out.push({ n: i % 2 === 0 ? i / 2 + 1 : null, san }));
		return out;
	}

	$: name = splitName(result.opening_name);
	$: family = name.family || result.archetype || '';
	$: score = pct(result.hybrid_score);
	$: plies = numbered(result.moves || '');
	$: white = pct(result.win_rate_white);
	$: black = pct(result.win_rate_black);
	$: draw = Math.max(0, 100 - white - black);
	$: panelId = `result-panel-${index}`;
</script>

<article class="entry" style="animation-delay: {index * 70}ms">
	<button
		type="button"
		class="summary"
		data-result-toggle
		aria-expanded={isExpanded}
		aria-controls={panelId}
		on:click={() => (isExpanded = !isExpanded)}
	>
		<span class="rank tabular" class:first={index === 0}>{String(index + 1).padStart(2, '0')}</span>

		<span class="body">
			{#if family}
				<span class="kicker family">{family}</span>
			{/if}
			<span class="title">{name.line}</span>
			{#if plies.length}
				<span class="moves">
					{#each plies as p}{#if p.n}<span class="move-no">{p.n}.</span>{/if}{p.san}{' '}{/each}
				</span>
			{/if}
		</span>

		<span class="score">
			<span class="score-value tabular">{score}</span>
			<span class="score-label">match</span>
			<span class="score-bar" aria-hidden="true"><span style="width: {score}%"></span></span>
		</span>

		<svg class="chevron" class:open={isExpanded} width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">
			<path d="M3 5l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5" />
		</svg>
	</button>

	{#if isExpanded}
		<div id={panelId} class="panel" transition:slide={{ duration: 320, easing: quintOut }}>
			<div class="panel-inner">
				{#if result.fen}
					<ChessBoard
						fen={result.fen}
						moves={result.moves}
						label="Position after {result.moves}"
					/>
				{/if}

				<div class="facts">
					<section>
						<h4 class="kicker">Results in the dataset</h4>
						<div class="outcome" aria-hidden="true">
							<span class="o-white" style="width: {white}%"></span>
							<span class="o-draw" style="width: {draw}%"></span>
							<span class="o-black" style="width: {black}%"></span>
						</div>
						<dl class="outcome-legend">
							<div><dt><i class="sw o-white"></i>White wins</dt><dd class="tabular">{white}%</dd></div>
							<div><dt><i class="sw o-draw"></i>Draw</dt><dd class="tabular">{draw}%</dd></div>
							<div><dt><i class="sw o-black"></i>Black wins</dt><dd class="tabular">{black}%</dd></div>
						</dl>
					</section>

					<section>
						<h4 class="kicker">Why it’s here</h4>
						<dl class="why">
							<div>
								<dt>Similar to your picks</dt>
								<dd class="tabular">{pct(result.cb_score)}</dd>
								<span class="meter" aria-hidden="true"><span style="width: {pct(result.cb_score)}%"></span></span>
							</div>
							<div>
								<dt>Played near your rating</dt>
								<dd class="tabular">{pct(result.cf_score)}</dd>
								<span class="meter" aria-hidden="true"><span style="width: {pct(result.cf_score)}%"></span></span>
							</div>
						</dl>
					</section>
				</div>
			</div>
		</div>
	{/if}
</article>

<style>
	.entry {
		border-top: 1px solid var(--rule);
		animation: rise 0.5s var(--ease) both;
	}

	.summary {
		display: grid;
		grid-template-columns: 3.25rem 1fr auto 14px;
		align-items: start;
		gap: 1.25rem;
		width: 100%;
		padding: 1.5rem 0.25rem;
		border: 0;
		background: transparent;
		color: inherit;
		font: inherit;
		text-align: left;
		cursor: pointer;
	}
	.summary:hover .title {
		text-decoration: underline;
		text-decoration-thickness: 1px;
		text-underline-offset: 4px;
	}

	.rank {
		font-family: var(--font-display);
		font-size: 2.25rem;
		line-height: 1;
		color: var(--ink-3);
	}
	.rank.first {
		color: var(--accent);
	}

	.body {
		display: grid;
		gap: 0.375rem;
		min-width: 0;
	}

	.title {
		font-family: var(--font-display);
		font-size: 1.375rem;
		line-height: 1.2;
		color: var(--ink);
		text-wrap: balance;
	}

	.moves {
		font-family: var(--font-mono);
		font-size: 0.875rem;
		color: var(--ink-2);
		word-spacing: 0.1em;
	}
	.move-no {
		color: var(--ink-3);
		margin-right: 0.1em;
	}

	.score {
		display: grid;
		justify-items: end;
		gap: 0.125rem;
		min-width: 4.5rem;
	}
	.score-value {
		font-family: var(--font-mono);
		font-size: 1.5rem;
		font-weight: 500;
		line-height: 1;
	}
	.score-label {
		font-size: 0.75rem;
		color: var(--ink-3);
	}
	.score-bar {
		width: 4.5rem;
		height: 3px;
		margin-top: 0.375rem;
		background: var(--rule);
	}
	.score-bar span {
		display: block;
		height: 100%;
		background: var(--ink);
	}

	.chevron {
		margin-top: 0.5rem;
		color: var(--ink-3);
		transition: transform 0.25s var(--ease);
	}
	.chevron.open {
		transform: rotate(180deg);
	}

	.panel-inner {
		display: grid;
		grid-template-columns: minmax(0, 300px) 1fr;
		gap: 2rem;
		padding: 0.25rem 0.25rem 2rem 4.5rem;
	}

	.facts {
		display: grid;
		align-content: start;
		gap: 1.75rem;
	}

	h4 {
		margin: 0 0 0.75rem;
	}

	.outcome {
		display: flex;
		height: 10px;
		border: 1px solid var(--ink);
	}
	/* Warna bidak tetap, tidak ikut tema: di mode gelap --ink justru terang */
	.o-white {
		background: #fbf8f2;
	}
	.o-draw {
		background: #8a8375;
	}
	.o-black {
		background: #1c1b18;
	}

	dl {
		margin: 0;
	}
	.outcome-legend {
		display: grid;
		gap: 0.375rem;
		margin-top: 0.75rem;
	}
	.outcome-legend div,
	.why div {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
		font-size: 0.875rem;
	}
	dt {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		color: var(--ink-2);
	}
	dd {
		margin: 0;
		font-family: var(--font-mono);
	}
	.sw {
		width: 10px;
		height: 10px;
		border: 1px solid var(--ink);
	}

	.why {
		display: grid;
		gap: 0.875rem;
	}
	.why div {
		flex-wrap: wrap;
	}
	.meter {
		flex-basis: 100%;
		height: 3px;
		background: var(--rule);
	}
	.meter span {
		display: block;
		height: 100%;
		background: var(--accent);
	}

	@media (max-width: 720px) {
		.summary {
			grid-template-columns: 2.25rem 1fr auto;
			gap: 0.875rem;
			padding: 1.25rem 0;
		}
		.chevron {
			display: none;
		}
		.rank {
			font-size: 1.625rem;
		}
		.title {
			font-size: 1.1875rem;
		}
		.score {
			min-width: 3rem;
		}
		.score-value {
			font-size: 1.25rem;
		}
		.score-bar {
			width: 3rem;
		}
		.panel-inner {
			grid-template-columns: 1fr;
			gap: 1.5rem;
			padding: 0 0 1.75rem;
		}
	}
</style>
