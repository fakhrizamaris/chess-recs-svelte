<script lang="ts">
  import { onMount } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import { toast } from 'svelte-sonner';
  import AnimatedSlider from '$lib/components/AnimatedSlider.svelte';
  import OpeningPicker from '$lib/components/OpeningPicker.svelte';
  import ResultCard from '$lib/components/ResultCard.svelte';
  import { getRecommendations, type RecommendationResponse } from '$lib/api/client';
  import { Sparkles, TrendingUp } from 'lucide-svelte';

  let eloRating = 1500;
  let favoriteOpenings: string[] = [];
  let alpha = 0.5;
  let results: RecommendationResponse[] = [];
  let isLoading = false;
  let hasSearched = false;

  async function handleSubmit() {
    if (favoriteOpenings.length === 0) {
      toast.error('Please select at least one favorite opening');
      return;
    }

    isLoading = true;
    hasSearched = true;
    results = [];

    try {
      const recommendations = await getRecommendations({
        user_rating: eloRating,
        favorite_openings: favoriteOpenings,
        alpha: alpha
      });

      results = recommendations;
      toast.success(`Found ${recommendations.length} perfect matches!`);
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Failed to get recommendations');
      console.error(error);
    } finally {
      isLoading = false;
    }
  }

  onMount(() => {
    fetch('http://localhost:3000/health')
      .then(res => res.text())
      .then(() => toast.success('Backend connected'))
      .catch(() => toast.error('Backend offline'));
  });
</script>

<svelte:head>
  <title>ChessRecs NextGen - AI Chess Recommendations</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</svelte:head>

<div class="min-h-screen pb-16">
  
  <!-- Header -->
  <header class="container mx-auto px-4 py-12">
    <div in:fly={{ y: -20, duration: 600, easing: quintOut }} class="text-center space-y-3">
      <div class="flex items-center justify-center gap-2 mb-2">
        <Sparkles class="w-6 h-6 text-primary-400" />
      </div>
      <h1 class="text-5xl md:text-6xl font-bold text-white mb-2">
        ChessRecs <span class="text-gradient">NextGen</span>
      </h1>
      <p class="text-lg text-white/60">
        AI-powered chess opening recommendations
      </p>
    </div>
  </header>

  <!-- Main Content -->
  <div class="container mx-auto px-4">
    <div class="grid lg:grid-cols-2 gap-6 items-start">
      
      <!-- Left: Input Form -->
      <div in:fly={{ x: -30, duration: 600, delay: 100 }}>
        <div class="glass-card rounded-2xl p-6 space-y-6 sticky top-6">
          <div class="flex items-center gap-2 border-b border-white/10 pb-4">
            <Sparkles class="w-5 h-5 text-primary-400" />
            <h2 class="text-xl font-semibold text-white">
              Your Preferences
            </h2>
          </div>

          <!-- ELO Rating Slider -->
          <AnimatedSlider
            bind:value={eloRating}
            min={500}
            max={3000}
            step={50}
            label="ELO Rating"
          />

          <!-- Favorite Openings -->
          <OpeningPicker bind:selected={favoriteOpenings} maxSelections={3} />

          <!-- Alpha Slider -->
          <AnimatedSlider
            bind:value={alpha}
            min={0}
            max={1}
            step={0.1}
            label="Algorithm Balance (α)"
          />

          <div class="glass p-3 rounded-lg text-xs text-white/50 space-y-0.5">
            <div><span class="text-white/70">α = 0:</span> Content-based</div>
            <div><span class="text-white/70">α = 1:</span> Collaborative</div>
            <div><span class="text-white/70">α = 0.5:</span> Balanced</div>
          </div>

          <!-- Submit Button -->
          <button
            on:click={handleSubmit}
            disabled={isLoading || favoriteOpenings.length === 0}
            class="glass-button w-full py-3.5 px-6 rounded-xl text-white font-semibold
                   disabled:opacity-40 disabled:cursor-not-allowed
                   flex items-center justify-center gap-2"
          >
            {#if isLoading}
              <div class="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
              Analyzing...
            {:else}
              <TrendingUp class="w-5 h-5" />
              Get Recommendations
            {/if}
          </button>
        </div>
      </div>

      <!-- Right: Results -->
      <div in:fly={{ x: 30, duration: 600, delay: 200 }}>
        {#if isLoading}
          <!-- Loading State -->
          <div class="space-y-4">
            {#each Array(5) as _, i}
              <div
                in:fade={{ delay: i * 80 }}
                class="h-40 glass rounded-xl animate-pulse"
              ></div>
            {/each}
          </div>
        {:else if results.length > 0}
          <!-- Results -->
          <div class="space-y-4">
            <div class="flex items-center gap-2 mb-4 pb-3 border-b border-white/10">
              <TrendingUp class="w-5 h-5 text-primary-400" />
              <h2 class="text-xl font-semibold text-white">
                Top Matches
              </h2>
            </div>

            {#each results as result, i (result.opening_name)}
              <ResultCard {result} index={i} />
            {/each}
          </div>
        {:else if hasSearched}
          <!-- No Results -->
<div
            in:fade
            class="glass-card rounded-xl p-12 text-center"
          >
            <div class="text-4xl mb-3 opacity-50">🤔</div>
            <p class="text-white/60">
              No recommendations found
            </p>
          </div>
        {:else}
          <!-- Empty State -->
          <div class="glass-card rounded-xl p-16 text-center">
            <div class="text-6xl mb-4 opacity-40">♟️</div>
            <h3 class="text-xl font-semibold text-white mb-2">
              Ready to Discover
            </h3>
            <p class="text-white/50">
              Fill in your preferences to get started
            </p>
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>