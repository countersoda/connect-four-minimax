<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { connectFourStore } from '../store/ConnectFour';

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'r' || event.key === 'R') {
			connectFourStore.createConnectFour($connectFourStore.mode);
		}
	}

	onMount(() => {
		if (typeof window !== 'undefined') window.addEventListener('keydown', handleKeyPress);
	});

	onDestroy(() => {
		if (typeof window !== 'undefined') window.removeEventListener('keydown', handleKeyPress);
	});
</script>

<button class="restart" on:click={() => connectFourStore.createConnectFour($connectFourStore.mode)}
	>Restart</button
>

<style>
	.restart {
		position: absolute;
		top: 10px;
		right: 10px;
		padding: 0.5rem 1rem;
		border-radius: 5px;
		border: solid darksalmon;
		color: darksalmon;
		margin-bottom: 2rem;
		transition: background-color 200ms ease-in-out;
		&:hover {
			background-color: darksalmon;
			color: white;
		}
	}
</style>
