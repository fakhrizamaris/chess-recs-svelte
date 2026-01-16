<script lang="ts">
  import { onMount } from 'svelte';
  import { Chess } from 'chess.js';

  export let fen: string;
  export let size: number = 280;
  export let showNotation: boolean = true;

  let squares: { file: string; rank: number; piece: string | null; color: 'light' | 'dark' }[] = [];

  const pieceUnicode: Record<string, string> = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
  };

  const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
  const ranks = [8, 7, 6, 5, 4, 3, 2, 1];

  function parseFen(fenString: string) {
    const result: typeof squares = [];
    
    try {
      const chess = new Chess(fenString);
      
      for (const rank of ranks) {
        for (const file of files) {
          const square = `${file}${rank}` as any;
          const piece = chess.get(square);
          const isLight = (files.indexOf(file) + rank) % 2 === 1;
          
          result.push({
            file,
            rank,
            piece: piece ? (piece.color === 'w' ? piece.type.toUpperCase() : piece.type.toLowerCase()) : null,
            color: isLight ? 'light' : 'dark'
          });
        }
      }
    } catch (e) {
      // Fallback to empty board
      for (const rank of ranks) {
        for (const file of files) {
          const isLight = (files.indexOf(file) + rank) % 2 === 1;
          result.push({ file, rank, piece: null, color: isLight ? 'light' : 'dark' });
        }
      }
    }
    
    return result;
  }

  $: squares = parseFen(fen);
  $: squareSize = size / 8;
  $: notationSize = showNotation ? 16 : 0;
  $: totalSize = size + notationSize;
</script>

<div class="board-container" style="width: {totalSize}px;">
  <!-- Top spacer for alignment -->
  {#if showNotation}
    <div class="notation-row" style="height: {notationSize}px; padding-left: {notationSize}px;">
      {#each files as file}
        <span class="file-label" style="width: {squareSize}px;">{file}</span>
      {/each}
    </div>
  {/if}

  <div class="board-row">
    <!-- Left rank labels -->
    {#if showNotation}
      <div class="rank-labels" style="width: {notationSize}px;">
        {#each ranks as rank}
          <span class="rank-label" style="height: {squareSize}px;">{rank}</span>
        {/each}
      </div>
    {/if}

    <!-- Chess Board -->
    <div 
      class="chess-board" 
      style="width: {size}px; height: {size}px; grid-template-columns: repeat(8, {squareSize}px);"
    >
      {#each squares as sq, i (i)}
        <div 
          class="square {sq.color}"
          style="width: {squareSize}px; height: {squareSize}px;"
        >
          {#if sq.piece}
            <span class="piece" class:white-piece={sq.piece === sq.piece.toUpperCase()}>
              {pieceUnicode[sq.piece]}
            </span>
          {/if}
        </div>
      {/each}
    </div>
  </div>

  <!-- Bottom file labels -->
  {#if showNotation}
    <div class="notation-row bottom" style="height: {notationSize}px; padding-left: {notationSize}px;">
      {#each files as file}
        <span class="file-label" style="width: {squareSize}px;">{file}</span>
      {/each}
    </div>
  {/if}
</div>

<style>
  .board-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .notation-row {
    display: flex;
    align-items: center;
  }

  .notation-row.bottom {
    margin-top: 2px;
  }

  .file-label {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.6);
    text-transform: uppercase;
  }

  .board-row {
    display: flex;
    align-items: stretch;
  }

  .rank-labels {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding-right: 4px;
  }

  .rank-label {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.6);
  }

  .chess-board {
    display: grid;
    border-radius: 4px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .square {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  .square.light {
    background: #f0d9b5;
  }

  .square.dark {
    background: #b58863;
  }

  .piece {
    font-size: 2rem;
    line-height: 1;
    user-select: none;
    filter: drop-shadow(1px 1px 1px rgba(0,0,0,0.3));
  }

  .white-piece {
    color: #fff;
    text-shadow: 
      0 0 2px #000,
      1px 1px 1px #000;
  }

  .piece:not(.white-piece) {
    color: #000;
  }

  /* Responsive font size */
  @media (max-width: 640px) {
    .piece {
      font-size: 1.5rem;
    }
    .file-label, .rank-label {
      font-size: 0.55rem;
    }
  }
</style>

