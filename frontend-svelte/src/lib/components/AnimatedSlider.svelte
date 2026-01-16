<script lang="ts">
  import { onMount } from 'svelte';

  export let value: number;
  export let min: number;
  export let max: number;
  export let step: number = 1;
  export let label: string;
  export let unit: string = '';

  let isVisible = false;

  onMount(() => {
    isVisible = true;
  });

  $: percentage = ((value - min) / (max - min)) * 100;
</script>

<div class="space-y-2">
  <div class="flex justify-between items-center">
    <label for="slider-{label}" class="text-sm font-medium text-white/70">
      {label}
    </label>
    <span
      class="text-xl font-bold text-primary-400 tabular-nums transition-all duration-300"
      class:scale-105={isVisible}
    >
      {value}{unit}
    </span>
  </div>

  <div class="relative">
    <!-- Track -->
    <div class="h-2 glass rounded-full overflow-hidden">
      <!-- Progress -->
      <div
        class="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full transition-all duration-300 ease-out"
        style="width: {percentage}%"
      ></div>
    </div>

    <!-- Slider Input -->
    <input
      id="slider-{label}"
      type="range"
      bind:value
      {min}
      {max}
      {step}
      class="absolute inset-0 w-full h-2 opacity-0 cursor-pointer z-10"
    />
  </div>

  <div class="flex justify-between text-xs text-white/40">
    <span>{min}{unit}</span>
    <span>{max}{unit}</span>
  </div>
</div>

<style>
  input[type="range"]::-webkit-slider-thumb {
    appearance: none;
    width: 20px;
    height: 20px;
    opacity: 1;
    background: linear-gradient(135deg, #60a5fa, #3b82f6);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
    transition: all 0.2s ease;
  }

  input[type="range"]::-webkit-slider-thumb:hover {
    transform: scale(1.15);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
  }

  input[type="range"]::-webkit-slider-thumb:active {
    transform: scale(0.95);
  }

  input[type="range"]::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #60a5fa, #3b82f6);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
    transition: all 0.2s ease;
  }
</style>