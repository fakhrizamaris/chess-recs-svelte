<script lang="ts">
  import { onMount } from 'svelte';
  import { Moon, Sun } from 'lucide-svelte';

  let isDark = false;

  function toggle() {
    isDark = !isDark;
    document.documentElement.classList.toggle('dark', isDark);
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }

  onMount(() => {
    isDark = localStorage.getItem('theme') === 'dark' ||
      window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.classList.toggle('dark', isDark);
  });
</script>

<button
  on:click={toggle}
  class="fixed top-4 right-4 p-3 bg-white dark:bg-gray-800 rounded-full shadow-lg
         hover:scale-110 transition-transform duration-200"
  aria-label="Toggle theme"
>
  {#if isDark}
    <Sun class="w-5 h-5 text-yellow-500" />
  {:else}
    <Moon class="w-5 h-5 text-gray-700" />
  {/if}
</button>
