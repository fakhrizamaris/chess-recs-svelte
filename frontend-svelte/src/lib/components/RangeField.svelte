<script lang="ts">
	export let id: string;
	export let value: number;
	export let min: number;
	export let max: number;
	export let step: number = 1;
	/** Teks yang dibacakan screen reader, mis. "1500, club player" */
	export let valueText: string | undefined = undefined;
	export let startLabel: string = '';
	export let endLabel: string = '';

	$: pct = ((value - min) / (max - min)) * 100;
</script>

<div class="range" style="--pct: {pct}%">
	<input
		{id}
		type="range"
		bind:value
		{min}
		{max}
		{step}
		aria-valuetext={valueText}
	/>
	{#if startLabel || endLabel}
		<div class="ends">
			<span>{startLabel}</span>
			<span>{endLabel}</span>
		</div>
	{/if}
</div>

<style>
	.range {
		display: grid;
		gap: 0.5rem;
	}

	input {
		-webkit-appearance: none;
		appearance: none;
		width: 100%;
		height: 28px;
		margin: 0;
		background: transparent;
		cursor: pointer;
	}

	/* Track: garis tipis tinta, bagian terisi berwarna aksen */
	input::-webkit-slider-runnable-track {
		height: 2px;
		background: linear-gradient(
			to right,
			var(--accent) 0 var(--pct),
			var(--rule-strong) var(--pct) 100%
		);
	}
	input::-moz-range-track {
		height: 2px;
		background: var(--rule-strong);
	}
	input::-moz-range-progress {
		height: 2px;
		background: var(--accent);
	}

	/* Thumb: satu petak papan */
	input::-webkit-slider-thumb {
		-webkit-appearance: none;
		appearance: none;
		width: 18px;
		height: 18px;
		margin-top: -8px;
		background: var(--ink);
		border: 3px solid var(--surface);
		box-shadow: 0 0 0 1px var(--ink);
		border-radius: 0;
		transition: transform 0.15s var(--ease), background-color 0.15s;
	}
	input::-moz-range-thumb {
		width: 12px;
		height: 12px;
		background: var(--ink);
		border: 3px solid var(--surface);
		box-shadow: 0 0 0 1px var(--ink);
		border-radius: 0;
	}

	input:hover::-webkit-slider-thumb,
	input:focus-visible::-webkit-slider-thumb {
		background: var(--accent);
		transform: scale(1.12);
	}
	input:hover::-moz-range-thumb,
	input:focus-visible::-moz-range-thumb {
		background: var(--accent);
	}

	input:focus-visible {
		outline-offset: 6px;
	}

	.ends {
		display: flex;
		justify-content: space-between;
		gap: 1rem;
		font-size: 0.8125rem;
		color: var(--ink-3);
	}
</style>
