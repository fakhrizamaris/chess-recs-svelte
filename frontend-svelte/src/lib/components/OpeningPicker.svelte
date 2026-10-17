<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { endpoints } from '$lib/api/client';

	export let selected: string[] = [];
	export let maxSelections: number = 3;
	/** Jumlah opening yang tersedia, untuk ditampilkan di halaman */
	export let total: number = 0;

	const MAX_VISIBLE = 50;
	const FALLBACK = [
		'Sicilian Defense', 'French Defense', 'Caro-Kann Defense', 'Italian Game',
		"Queen's Gambit", "King's Indian Defense", 'English Opening', 'Ruy Lopez',
		'Scandinavian Defense', 'Nimzo-Indian Defense', 'Pirc Defense'
	];

	let openings: string[] = [];
	let query = '';
	let isOpen = false;
	let isLoading = true;
	let loadFailed = false;
	let activeIndex = 0;
	let listEl: HTMLUListElement;

	onMount(async () => {
		try {
			const response = await fetch(endpoints.openings());
			if (!response.ok) throw new Error(`HTTP ${response.status}`);
			const data = await response.json();
			openings = data.openings || [];
		} catch (error) {
			console.error('Failed to load openings:', error);
			openings = FALLBACK;
			loadFailed = true;
		} finally {
			total = openings.length;
			isLoading = false;
		}
	});

	/**
	 * Urutkan berdasarkan relevansi, bukan alfabet:
	 * nama persis > awalan nama > awal kata > mengandung. Seri dipecah dengan nama terpendek.
	 * Tanpa kata kunci, tampilkan hanya opening induk (tanpa varian) agar daftar awal ringkas.
	 */
	function rank(list: string[], q: string, exclude: string[]) {
		const needle = q.trim().toLowerCase();
		const pool = list.filter((o) => !exclude.includes(o));
		if (!needle) return pool.filter((o) => !o.includes(':') && !o.includes('|'));

		const scored: { name: string; score: number }[] = [];
		for (const name of pool) {
			const hay = name.toLowerCase();
			const at = hay.indexOf(needle);
			if (at === -1) continue;
			let score = 3;
			if (hay === needle) score = 0;
			else if (at === 0) score = 1;
			else if (/[\s:(|-]/.test(hay[at - 1])) score = 2;
			scored.push({ name, score });
		}
		scored.sort((a, b) => a.score - b.score || a.name.length - b.name.length || a.name.localeCompare(b.name));
		return scored.map((s) => s.name);
	}

	$: matches = rank(openings, query, selected);
	$: visible = matches.slice(0, MAX_VISIBLE);
	$: isFull = selected.length >= maxSelections;
	$: if (activeIndex >= visible.length) activeIndex = Math.max(0, visible.length - 1);

	function split(name: string, q: string) {
		const at = q ? name.toLowerCase().indexOf(q.trim().toLowerCase()) : -1;
		if (at === -1) return [name, '', ''];
		const end = at + q.trim().length;
		return [name.slice(0, at), name.slice(at, end), name.slice(end)];
	}

	function add(name: string) {
		if (isFull || selected.includes(name)) return;
		selected = [...selected, name];
		query = '';
		activeIndex = 0;
		// Tutup agar daftar tidak menutupi field berikutnya; mengetik atau ↓ membukanya lagi
		isOpen = false;
	}

	function remove(name: string) {
		selected = selected.filter((o) => o !== name);
	}

	async function move(delta: number) {
		if (!visible.length) return;
		isOpen = true;
		activeIndex = (activeIndex + delta + visible.length) % visible.length;
		await tick();
		listEl?.querySelector(`[data-index="${activeIndex}"]`)?.scrollIntoView({ block: 'nearest' });
	}

	function onKeydown(e: KeyboardEvent) {
		if (e.key === 'ArrowDown') {
			e.preventDefault();
			move(1);
		} else if (e.key === 'ArrowUp') {
			e.preventDefault();
			move(-1);
		} else if (e.key === 'Enter') {
			if (isOpen && visible[activeIndex]) {
				e.preventDefault();
				add(visible[activeIndex]);
			}
		} else if (e.key === 'Escape') {
			isOpen = false;
		} else if (e.key === 'Backspace' && !query && selected.length) {
			remove(selected[selected.length - 1]);
		}
	}
</script>

<div class="picker">
	{#if selected.length > 0}
		<ul class="chips" aria-label="Selected openings">
			{#each selected as name, i (name)}
				<li class="chip">
					<span class="chip-index tabular">{i + 1}</span>
					<span class="chip-name">{name}</span>
					<button type="button" class="chip-remove" on:click={() => remove(name)} aria-label="Remove {name}">
						<svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true"
							><path d="M1 1l8 8M9 1L1 9" stroke="currentColor" stroke-width="1.6" /></svg
						>
					</button>
				</li>
			{/each}
		</ul>
	{/if}

	<div class="field">
		<svg class="field-icon" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true">
			<circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.5" />
			<path d="M11 11l3.5 3.5" stroke="currentColor" stroke-width="1.5" />
		</svg>
		<input
			id="opening-search"
			type="text"
			role="combobox"
			autocomplete="off"
			spellcheck="false"
			aria-autocomplete="list"
			aria-expanded={isOpen && visible.length > 0}
			aria-controls="opening-listbox"
			aria-activedescendant={isOpen && visible[activeIndex] ? `opening-option-${activeIndex}` : undefined}
			aria-describedby="opening-hint"
			bind:value={query}
			on:focus={() => (isOpen = true)}
			on:input={() => {
				isOpen = true;
				activeIndex = 0;
			}}
			on:blur={() => (isOpen = false)}
			on:keydown={onKeydown}
			placeholder={isLoading
				? 'Loading openings…'
				: isFull
					? 'Remove one to choose another'
					: 'Search, e.g. Caro-Kann'}
			disabled={isLoading || isFull}
		/>
		{#if isLoading}
			<span class="spinner" aria-hidden="true"></span>
		{/if}

		{#if isOpen && !isFull}
			<div class="popover">
				{#if visible.length > 0}
					<!-- mousedown dicegah agar input tidak blur sebelum klik terdaftar -->
					<ul
						id="opening-listbox"
						role="listbox"
						aria-label="Openings"
						bind:this={listEl}
						on:mousedown|preventDefault
					>
						{#each visible as name, i (name)}
							{@const [pre, hit, post] = split(name, query)}
							<!-- Keyboard ditangani di input (pola combobox + aria-activedescendant) -->
							<!-- svelte-ignore a11y_click_events_have_key_events -->
							<li
								id="opening-option-{i}"
								role="option"
								aria-selected={i === activeIndex}
								data-index={i}
								class:active={i === activeIndex}
								on:click={() => add(name)}
								on:mousemove={() => (activeIndex = i)}
							>
								<span>{pre}<mark>{hit}</mark>{post}</span>
							</li>
						{/each}
					</ul>
					<p class="popover-foot">
						{#if matches.length > MAX_VISIBLE}
							Showing {MAX_VISIBLE} of {matches.length}. Keep typing to narrow it down.
						{:else if !query}
							Main lines only. Type to search all {openings.length} variations.
						{:else}
							{matches.length} {matches.length === 1 ? 'match' : 'matches'}
						{/if}
					</p>
				{:else if query}
					<p class="popover-empty">No opening matches “{query}”.</p>
				{/if}
			</div>
		{/if}
	</div>

	<p id="opening-hint" class="hint">
		{#if loadFailed}
			Couldn’t reach the server, so only a short list is available.
		{:else if isFull}
			That’s {maxSelections}. Remove one to swap it out.
		{:else}
			Pick up to {maxSelections}.<span class="kbd-hint"> Use ↑ ↓ and Enter to choose.</span>
		{/if}
	</p>
</div>

<style>
	.picker {
		display: grid;
		gap: 0.75rem;
	}

	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		margin: 0;
		padding: 0;
		list-style: none;
	}

	.chip {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		max-width: 100%;
		padding: 0.375rem 0.375rem 0.375rem 0.5rem;
		background: var(--ink);
		color: var(--paper);
		font-size: 0.875rem;
		animation: rise 0.3s var(--ease) both;
	}

	.chip-index {
		font-family: var(--font-mono);
		font-size: 0.6875rem;
		color: var(--accent-soft);
	}

	.chip-name {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.chip-remove {
		display: grid;
		place-items: center;
		width: 22px;
		height: 22px;
		flex-shrink: 0;
		border: 0;
		background: transparent;
		color: inherit;
		opacity: 0.7;
		cursor: pointer;
	}
	.chip-remove:hover {
		opacity: 1;
		background: var(--accent);
	}

	/* relative: dropdown terkunci ke lebar & posisi input ini */
	.field {
		position: relative;
	}

	.field-icon {
		position: absolute;
		left: 0.875rem;
		top: 50%;
		transform: translateY(-50%);
		color: var(--ink-3);
		pointer-events: none;
	}

	input {
		width: 100%;
		padding: 0.8125rem 2.75rem;
		background: var(--surface);
		border: 1px solid var(--rule-strong);
		border-radius: var(--radius);
		color: var(--ink);
		font: inherit;
		font-size: 1rem;
		transition: border-color 0.15s, box-shadow 0.15s;
	}
	input::placeholder {
		color: var(--ink-3);
	}
	input:hover:not(:disabled) {
		border-color: var(--ink);
	}
	input:focus {
		outline: none;
		border-color: var(--ink);
		box-shadow: 0 0 0 1px var(--ink);
	}
	input:disabled {
		cursor: not-allowed;
		opacity: 0.7;
	}

	.spinner {
		position: absolute;
		right: 0.875rem;
		top: 50%;
		width: 14px;
		height: 14px;
		margin-top: -7px;
		border: 1.5px solid var(--rule);
		border-top-color: var(--ink);
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}
	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	/* Latar penuh (tanpa transparansi/blur) supaya tidak ada teks yang tembus */
	.popover {
		position: absolute;
		z-index: 30;
		top: calc(100% + 4px);
		left: 0;
		right: 0;
		background: var(--surface);
		border: 1px solid var(--ink);
		box-shadow: 4px 4px 0 var(--ink);
		animation: rise 0.18s var(--ease) both;
	}

	ul[role='listbox'] {
		max-height: min(320px, 50vh);
		overflow-y: auto;
		margin: 0;
		padding: 0.25rem 0;
		list-style: none;
		overscroll-behavior: contain;
	}

	li[role='option'] {
		padding: 0.625rem 0.875rem;
		font-size: 0.9375rem;
		line-height: 1.35;
		color: var(--ink-2);
		cursor: pointer;
		border-left: 3px solid transparent;
	}
	li[role='option'].active {
		background: var(--paper);
		color: var(--ink);
		border-left-color: var(--accent);
	}

	mark {
		background: none;
		color: var(--ink);
		font-weight: 600;
		text-decoration: underline;
		text-decoration-color: var(--accent);
		text-decoration-thickness: 2px;
		text-underline-offset: 3px;
	}

	.popover-foot,
	.popover-empty {
		margin: 0;
		padding: 0.5rem 0.875rem;
		font-size: 0.75rem;
		color: var(--ink-3);
		border-top: 1px solid var(--rule);
	}
	.popover-empty {
		border-top: 0;
		padding: 1rem 0.875rem;
		font-size: 0.875rem;
	}

	.hint {
		margin: 0;
		font-size: 0.8125rem;
		color: var(--ink-3);
	}
	/* Petunjuk keyboard tidak relevan di layar sentuh */
	@media (pointer: coarse) {
		.kbd-hint {
			display: none;
		}
	}
</style>
