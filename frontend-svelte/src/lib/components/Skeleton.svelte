<script lang="ts">
  export let className: string = '';
</script>

<div class="bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 dark:from-gray-700 dark:via-gray-600 dark:to-gray-700
         animate-[shimmer_2s_infinite] {className}"></div>

<style>
  @keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
  }

  div {
    background-size: 1000px 100%;
  }
</style>