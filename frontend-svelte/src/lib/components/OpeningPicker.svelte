<script lang="ts">
  import { Search } from 'lucide-svelte';
  import { fly, scale } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import { onMount } from 'svelte';

  export let selected: string[] = [];
  export let maxSelections: number = 3;

  let openings: string[] = [];
  let searchQuery = '';
  let isOpen = false;
  let isLoading = true;

  // Load openings from API
  onMount(async () => {
    try {
      const response = await fetch('http://localhost:8001/openings');
      const data = await response.json();
      openings = data.openings || [];
      isLoading = false;
    } catch (error) {
      console.error('Failed to load openings:', error);
      // Fallback to hardcoded list
      openings = [
        'Sicilian Defense', 'French Defense', 'Caro-Kann Defense',
        'Italian Game', 'Spanish Opening', 'Queen\'s Gambit',
        'King\'s Indian Defense', 'English Opening', 'Ruy Lopez',
        'Scandinavian Defense', 'Nimzo-Indian Defense', 'Pirc Defense'
      ];
      isLoading = false;
    }
  });

  $: filtered = openings.filter(opening =>
    opening.toLowerCase().includes(searchQuery.toLowerCase()) &&
    !selected.includes(opening)
  );

  function toggle(opening: string) {
    if (selected.includes(opening)) {
      selected = selected.filter(o => o !== opening);
    } else if (selected.length < maxSelections) {
      selected = [...selected, opening];
      searchQuery = ''; // Clear search after selection
    }
  }

  function remove(opening: string) {
    selected = selected.filter(o => o !== opening);
  }
</script>

<div class="space-y-3">
  <label for="opening-search" class="text-sm font-semibold text-white/90">
    Favorite Openings ({selected.length}/{maxSelections})
  </label>

  <!-- Selected Items -->
  {#if selected.length > 0}
    <div class="flex flex-wrap gap-2">
      {#each selected as opening (opening)}
        <div
          in:scale={{ duration: 200, easing: quintOut }}
          out:scale={{ duration: 150 }}
          class="flex items-center gap-2 px-4 py-2 glass rounded-full text-sm font-medium text-white
                 hover:bg-white/10 transition-all group"
        >
          <span>{opening}</span>
          <button
            on:click={() => remove(opening)}
            class="w-5 h-5 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center
                   transition-all group-hover:rotate-90"
            aria-label="Remove {opening}"
          >
            ×
          </button>
        </div>
      {/each}
    </div>
  {/if}

  <!-- Search Input -->
  <div class="relative">
    <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-white/60" />
    <input
      id="opening-search"
      type="text"
      bind:value={searchQuery}
      on:focus={() => isOpen = true}
      on:blur={() => setTimeout(() => isOpen = false, 200)}
      placeholder={isLoading ? "Loading openings..." : "Search openings..."}
      class="glass-input w-full pl-11 pr-4 py-3.5 rounded-xl text-white placeholder-white/50
             transition-all focus:ring-2 focus:ring-primary-500/50"
      disabled={selected.length >= maxSelections || isLoading}
    />
    {#if isLoading}
      <div class="absolute right-3 top-1/2 -translate-y-1/2">
        <div class="w-5 h-5 border-2 border-white/20 border-t-white/60 rounded-full animate-spin"></div>
      </div>
    {/if}
  </div>

  <!-- Dropdown Results -->
  {#if isOpen && filtered.length > 0}
    <div
      in:fly={{ y: -10, duration: 200 }}
      out:fly={{ y: -10, duration: 150 }}
      class="absolute z-50 w-full mt-1 glass-card rounded-xl max-h-80 overflow-y-auto"
    >
      <div class="p-2 space-y-1">
        {#each filtered as opening (opening)}
          <button
            on:click={() => toggle(opening)}
            class="w-full px-4 py-3 text-left text-white/90 rounded-lg
                   hover:bg-white/10 transition-all text-sm
                   flex items-center justify-between group"
          >
            <span>{opening}</span>
            <span class="text-xs text-white/40 group-hover:text-primary-400 transition-colors">
              Click to add
            </span>
          </button>
        {/each}
      </div>
    </div>
  {:else if isOpen && searchQuery && filtered.length === 0}
    <div
      in:fly={{ y: -10, duration: 200 }}
      class="absolute z-50 w-full mt-1 glass-card rounded-xl p-4"
    >
      <p class="text-white/60 text-sm text-center">
        No openings found for "{searchQuery}"
      </p>
    </div>
  {/if}

  <!-- Preview hint -->
  {#if !isOpen && openings.length > 0 && selected.length < maxSelections}
    <p class="text-xs text-white/50">
      Click to browse {openings.length} available openings
    </p>
  {/if}
</div>