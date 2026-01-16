<script lang="ts">
  import { fly, scale, slide } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import type { RecommendationResponse } from '$lib/api/client';
  import { Star, ChevronDown, ChevronUp } from 'lucide-svelte';
  import ChessBoard from './ChessBoard.svelte';

  export let result: RecommendationResponse;
  export let index: number;

  let isExpanded = false;
  let isHovered = false;

  $: delay = index * 100;
  $: scorePercent = Math.round(result.hybrid_score * 100);

  function toggleExpand() {
    isExpanded = !isExpanded;
  }
</script>

<div
  role="article"
  in:fly={{ y: 20, duration: 400, delay, easing: quintOut }}
  out:scale={{ duration: 200 }}
  on:mouseenter={() => isHovered = true}
  on:mouseleave={() => isHovered = false}
  class="group relative glass-card rounded-xl overflow-hidden transition-all duration-300"
  class:scale-[1.01]={isHovered}
>
  <!-- Score badge -->
  <div
    class="absolute -top-1.5 -right-3 w-16 h-16 rounded-xl flex items-center justify-center z-10
           bg-gradient-to-br from-primary-500 to-primary-600
           shadow-lg transition-transform duration-300"
    class:rotate-3={isHovered}
  >
    <div class="text-center">
      <Star class="w-3.5 h-3.5 text-white/80 mx-auto mb-0.5" />
      <div class="text-xl font-bold text-white">{scorePercent}</div>
    </div>
  </div>

  <!-- Collapsed View (Always Visible) -->
  <button
    on:click={toggleExpand}
    class="w-full text-left p-5 pr-20 flex items-center justify-between gap-4
           hover:bg-white/5 transition-colors cursor-pointer"
  >
    <div class="flex-1 space-y-2">
      <h3 class="text-lg font-semibold text-white group-hover:text-primary-400 transition-colors">
        {result.opening_name}
      </h3>

      {#if result.archetype}
        <div class="inline-flex items-center px-3 py-1 glass rounded-full text-xs font-medium text-white/80">
          <span class="w-1.5 h-1.5 rounded-full bg-primary-400 mr-2"></span>
          {result.archetype}
        </div>
      {/if}
    </div>

    <!-- Expand/Collapse Icon -->
    <div class="text-white/60 transition-transform duration-300" class:rotate-180={isExpanded}>
      {#if isExpanded}
        <ChevronUp class="w-6 h-6" />
      {:else}
        <ChevronDown class="w-6 h-6" />
      {/if}
    </div>
  </button>

  <!-- Expanded View (Collapsible) -->
  {#if isExpanded}
    <div 
      transition:slide={{ duration: 400, easing: quintOut }}
      class="border-t border-white/10 bg-white/5"
    >
      <div class="p-5 space-y-4">
        
        <!-- Chess Board - Local Rendering (No External API) -->
        {#if result.fen}
          <div class="flex justify-center glass rounded-lg p-3">
            <ChessBoard fen={result.fen} size={280} />
          </div>
        {/if}

        <!-- Opening Moves -->
        {#if result.moves}
          <div class="glass p-3 rounded-lg">
            <div class="text-xs text-white/50 mb-1">Opening Moves:</div>
            <div class="text-sm text-white/80 font-mono">
              {result.moves}
            </div>
          </div>
        {/if}

        <!-- Win Rates -->
        <div class="grid grid-cols-3 gap-3">
          <div class="glass p-3 rounded-lg text-center">
            <div class="text-xs text-white/50 mb-1">White</div>
            <div class="text-lg font-bold text-white">
              {Math.round(result.win_rate_white * 100)}%
            </div>
          </div>
          <div class="glass p-3 rounded-lg text-center">
            <div class="text-xs text-white/50 mb-1">Black</div>
            <div class="text-lg font-bold text-white">
              {Math.round(result.win_rate_black * 100)}%
            </div>
          </div>
          <div class="glass p-3 rounded-lg text-center">
            <div class="text-xs text-white/50 mb-1">Draw</div>
            <div class="text-lg font-bold text-white">
              {Math.round(result.win_rate_draw * 100)}%
            </div>
          </div>
        </div>

        <!-- Score Breakdown -->
        <div class="glass p-3 rounded-lg space-y-2">
          <div class="text-xs text-white/50 mb-2">Score Breakdown:</div>
          
          <div class="flex justify-between items-center text-sm">
            <span class="text-white/70">Content-Based:</span>
            <span class="text-white font-medium">{Math.round(result.cb_score * 100)}%</span>
          </div>
          
          <div class="flex justify-between items-center text-sm">
            <span class="text-white/70">Collaborative:</span>
            <span class="text-white font-medium">{Math.round(result.cf_score * 100)}%</span>
          </div>
          
          <div class="h-px bg-white/10 my-2"></div>
          
          <div class="flex justify-between items-center text-sm">
            <span class="text-white font-semibold">Hybrid Score:</span>
            <span class="text-primary-400 font-bold">{scorePercent}%</span>
          </div>
        </div>

      </div>
    </div>
  {/if}

  <!-- Subtle hover effect -->
  <div
    class="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
    style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), transparent);"
  ></div>
</div>
