<script lang="ts">
  import { onMount } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import { toast } from 'svelte-sonner';
  import AnimatedSlider from '$lib/components/AnimatedSlider.svelte';
  import OpeningPicker from '$lib/components/OpeningPicker.svelte';
  import ResultCard from '$lib/components/ResultCard.svelte';
  import { getRecommendations, endpoints, type RecommendationResponse } from '$lib/api/client';
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
    // Silent health check - no toast for users
    fetch(endpoints.health())
      .then(res => res.text())
      .then(() => console.log('✅ Backend connected'))
      .catch(() => console.warn('⚠️ Backend offline'));
  });
</script>

<svelte:head>
  <title>ChessRecs NextGen - Smart Chess Opening Recommendations</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</svelte:head>

<div class="min-h-screen pb-16">
  
  <!-- Enhanced Header -->
  <header class="relative overflow-hidden">
    <!-- Background decoration -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute top-10 left-10 text-8xl animate-pulse">♔</div>
      <div class="absolute top-20 right-20 text-7xl animate-pulse delay-300">♕</div>
      <div class="absolute bottom-10 left-1/4 text-6xl animate-pulse delay-500">♘</div>
      <div class="absolute bottom-5 right-1/3 text-5xl animate-pulse delay-700">♗</div>
    </div>
    
    <div class="container mx-auto px-4 py-16 relative z-10">
      <div in:fly={{ y: -20, duration: 600, easing: quintOut }} class="text-center space-y-4">
        <!-- Logo/Icon -->
        <div class="flex items-center justify-center gap-3 mb-4">
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center shadow-lg shadow-primary-500/30">
            <span class="text-2xl">♟</span>
          </div>
        </div>
        
        <!-- Title with animated gradient -->
        <h1 class="text-5xl md:text-7xl font-bold text-white mb-3 tracking-tight">
          ChessRecs <span class="text-gradient bg-gradient-to-r from-primary-400 via-purple-400 to-primary-400 bg-clip-text text-transparent bg-[length:200%_auto] animate-gradient">NextGen</span>
        </h1>
        
        <!-- Subtitle -->
        <p class="text-lg md:text-xl text-white/60 max-w-md mx-auto">
          Discover your next favorite opening with smart recommendations
        </p>
        
        <!-- Stats badges -->
        <div class="flex items-center justify-center gap-4 mt-6">
          <div class="glass px-4 py-2 rounded-full text-sm text-white/70 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
            500+ Openings
          </div>
          <div class="glass px-4 py-2 rounded-full text-sm text-white/70">
            Hybrid Algorithm
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <div class="container mx-auto px-4 max-w-2xl">
    
    <!-- Input Form -->
    <div in:fly={{ y: 20, duration: 600, delay: 100 }} class="mb-8">
      <div class="glass-card rounded-2xl p-6 space-y-6">
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
          <div><span class="text-white/70">α = 1:</span> Content-based</div>
          <div><span class="text-white/70">α = 0:</span> Collaborative</div>
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

    <!-- Results Section (Below Preferences) -->
    <div in:fly={{ y: 20, duration: 600, delay: 200 }}>
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

  <!-- How It Works Section -->
  <section class="container mx-auto px-4 max-w-4xl mt-16 mb-12">
    <h2 class="text-2xl font-bold text-white text-center mb-8">How It Works</h2>
    <div class="grid md:grid-cols-3 gap-6">
      <div class="glass-card rounded-xl p-6 text-center">
        <div class="text-3xl mb-3">🎯</div>
        <h3 class="font-semibold text-white mb-2">Set Your Rating</h3>
        <p class="text-sm text-white/60">Enter your ELO rating to get openings matched to your skill level.</p>
      </div>
      <div class="glass-card rounded-xl p-6 text-center">
        <div class="text-3xl mb-3">♟️</div>
        <h3 class="font-semibold text-white mb-2">Pick Favorites</h3>
        <p class="text-sm text-white/60">Select up to 3 openings you already enjoy playing.</p>
      </div>
      <div class="glass-card rounded-xl p-6 text-center">
        <div class="text-3xl mb-3">✨</div>
        <h3 class="font-semibold text-white mb-2">Get Recommendations</h3>
        <p class="text-sm text-white/60">Discover new openings tailored to your style and preferences.</p>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="border-t border-white/10 mt-auto">
    <div class="container mx-auto px-4 py-8">
      <!-- Main footer row with grid for proper centering -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-center text-center">
        <!-- Left: Brand -->
        <div class="md:text-left">
          <p class="text-white/80 font-semibold">ChessRecs NextGen</p>
          <p class="text-sm text-white/50">Built with Hybrid Recommendation System</p>
        </div>
        
        <!-- Center: Tech Stack + GitHub -->
        <div class="flex items-center justify-center gap-3">
          <div class="flex items-center gap-2">
            <span class="px-2 py-1 glass rounded text-xs text-white/60">Svelte</span>
            <span class="px-2 py-1 glass rounded text-xs text-white/60">Rust</span>
            <span class="px-2 py-1 glass rounded text-xs text-white/60">Python</span>
          </div>
          <a 
            href="https://github.com/fakhrizamaris/chess-recs-svelte" 
            target="_blank" 
            rel="noopener noreferrer"
            class="px-3 py-1.5 glass rounded-lg text-xs text-white/70 hover:text-white hover:bg-white/10 transition-all flex items-center gap-1.5"
            title="View on GitHub"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            GitHub
          </a>
        </div>
        
        <!-- Right: Copyright -->
        <p class="text-xs text-white/40 md:text-right">
          © {new Date().getFullYear()} All rights reserved
        </p>
      </div>
      
      <!-- Dataset Credit -->
      <div class="mt-6 pt-4 border-t border-white/5 text-center">
        <p class="text-xs text-white/30">
          Dataset: <a 
            href="https://www.kaggle.com/datasets/datasnaek/chess" 
            target="_blank" 
            rel="noopener noreferrer"
            class="text-primary-400/70 hover:text-primary-400 underline underline-offset-2 transition-colors"
          >Chess Game Dataset (Lichess)</a> on Kaggle
        </p>
      </div>
    </div>
  </footer>
</div>