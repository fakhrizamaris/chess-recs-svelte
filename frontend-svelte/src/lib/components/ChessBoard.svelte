<script lang="ts">
	import { Chess, type Square } from 'chess.js';

	export let fen: string;
	/** Langkah SAN (mis. "e4 c5 Nf3"), dipakai untuk menandai langkah terakhir */
	export let moves: string = '';
	export let label: string = 'Chess position';

	type Cell = { square: string; piece: string | null; white: boolean; light: boolean };

	// Glyph penuh untuk kedua warna; warna putih diberi isi terang + garis tinta.
	// Tiap glyph diikuti U+FE0E (variation selector) agar tampil sebagai teks,
	// bukan emoji (iOS merender ♟ sebagai emoji).
	const glyph: Record<string, string> = {
		k: '♚︎', q: '♛︎', r: '♜︎',
		b: '♝︎', n: '♞︎', p: '♟︎'
	};
	const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
	const ranks = [8, 7, 6, 5, 4, 3, 2, 1];

	function build(fenString: string): Cell[] {
		let chess: Chess | null = null;
		try {
			chess = new Chess(fenString);
		} catch {
			chess = null;
		}
		const cells: Cell[] = [];
		for (const rank of ranks) {
			for (const [fi, file] of files.entries()) {
				const square = `${file}${rank}`;
				const p = chess?.get(square as Square);
				cells.push({
					square,
					piece: p ? p.type : null,
					white: p ? p.color === 'w' : false,
					light: (fi + rank) % 2 === 1
				});
			}
		}
		return cells;
	}

	function lastMove(sanMoves: string): string[] {
		const list = sanMoves.split(/\s+/).filter((m) => m && !/^\d+\.+$/.test(m));
		if (!list.length) return [];
		try {
			const chess = new Chess();
			let last = null;
			for (const san of list) last = chess.move(san);
			return last ? [last.from, last.to] : [];
		} catch {
			return [];
		}
	}

	$: cells = build(fen);
	$: marked = lastMove(moves);
</script>

<div class="board" role="img" aria-label={label}>
	{#each cells as c (c.square)}
		<div class="sq" class:light={c.light} class:mark={marked.includes(c.square)}>
			{#if c.square[0] === 'a'}
				<span class="coord rank">{c.square[1]}</span>
			{/if}
			{#if c.square[1] === '1'}
				<span class="coord file">{c.square[0]}</span>
			{/if}
			{#if c.piece}
				<span class="piece" class:white={c.white}>{glyph[c.piece]}</span>
			{/if}
		</div>
	{/each}
</div>

<style>
	.board {
		display: grid;
		/* Baris & kolom eksplisit: tanpa ini baris berisi bidak lebih tinggi dari baris kosong */
		grid-template-columns: repeat(8, minmax(0, 1fr));
		grid-template-rows: repeat(8, minmax(0, 1fr));
		width: 100%;
		max-width: 360px;
		aspect-ratio: 1;
		border: 1px solid var(--ink);
		container-type: inline-size;
	}

	.sq {
		position: relative;
		display: grid;
		place-items: center;
		min-height: 0;
		overflow: hidden;
		background: var(--board-dark);
		color: var(--board-light);
	}
	.sq.light {
		background: var(--board-light);
		color: var(--board-dark);
	}
	/* Langkah terakhir: lapisan aksen di atas warna petak */
	.sq.mark {
		background-image: linear-gradient(var(--board-mark), var(--board-mark));
	}

	.coord {
		position: absolute;
		font-family: var(--font-mono);
		font-size: max(8px, 2.6cqi);
		font-weight: 500;
		line-height: 1;
	}
	.coord.rank {
		top: 3px;
		left: 3px;
	}
	.coord.file {
		right: 3px;
		bottom: 2px;
	}

	.piece {
		font-family: 'Segoe UI Symbol', 'Apple Symbols', 'DejaVu Sans', 'Noto Sans Symbols 2', serif;
		font-size: 9.6cqi;
		line-height: 1;
		color: #1c1b18;
		user-select: none;
		transform: translateY(-3%);
	}
	.piece.white {
		color: #fbf8f2;
		-webkit-text-stroke: 0.045em #1c1b18;
		paint-order: stroke fill;
	}
</style>
