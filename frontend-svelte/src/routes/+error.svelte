<script lang="ts">
	import { page } from '$app/stores';
	import Logo from '$lib/components/Logo.svelte';
</script>

<svelte:head>
	<title>{$page.status} · ChessRecs</title>
</svelte:head>

<main class="error">
	<Logo size={40} />
	<p class="kicker">Error {$page.status}</p>
	<h1>{$page.status === 404 ? 'This square is empty.' : 'Something went wrong.'}</h1>
	<p class="message">{$page.error?.message || 'An unexpected error occurred.'}</p>
	<a href="/">Back to the board</a>
</main>

<style>
	.error {
		position: relative;
		z-index: 1;
		display: grid;
		justify-items: start;
		gap: 1rem;
		max-width: 34rem;
		margin: 0 auto;
		padding: clamp(4rem, 15vh, 9rem) 1.5rem;
	}
	h1 {
		margin: 0;
		font-family: var(--font-display);
		font-weight: 400;
		font-size: clamp(2.25rem, 6vw, 3.5rem);
		line-height: 1.05;
	}
	.message {
		margin: 0;
		color: var(--ink-2);
	}
	a {
		margin-top: 0.5rem;
		font-weight: 600;
		color: var(--accent);
		text-underline-offset: 4px;
	}
</style>
