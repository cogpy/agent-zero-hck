import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			fallback: 'index.html',  // SPA mode for client-side routing
			strict: false  // Allow dynamic routes
		})
	},
	preprocess: vitePreprocess()
};

export default config;
