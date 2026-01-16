<script lang="ts">
  import { page } from '$app/stores';
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
  <div class="text-center space-y-4">
    <h1 class="text-6xl font-bold text-gray-900 dark:text-white">
      {$page.status}
    </h1>
    <p class="text-xl text-gray-600 dark:text-gray-400">
      {$page.error?.message || 'Something went wrong'}
    </p>
    <a
      href="/"
      class="inline-block px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
    >
      Go Home
    </a>
  </div>
</div>