<script lang="ts">
	import { Toaster } from 'svelte-sonner';
	import '../app.css';
</script>

<Toaster
	position="bottom-center"
	toastOptions={{
		style:
			'background: var(--ink); color: var(--paper); border: 0; border-radius: 2px; font-family: var(--font-body); font-size: 0.9375rem;'
	}}
/>
<slot />
