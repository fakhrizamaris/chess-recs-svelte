<script lang="ts">
	/** Lintasan langkah kuda (L) yang berakhir di kotak tujuan: "langkah berikutnya". */
	export let size: number = 28;
	export let title: string = 'ChessRecs';
</script>

<svg width={size} height={size} viewBox="0 0 32 32" role="img" aria-label={title}>
	<path d="M9 29V9h9" fill="none" stroke="currentColor" stroke-width="5.5" stroke-linejoin="miter" />
	<rect x="17.5" y="3" width="11.5" height="11.5" fill="var(--accent)" />
</svg>
