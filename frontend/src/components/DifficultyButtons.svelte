<script lang="ts">
	import { connectFourStore } from '../store/ConnectFour';
	$: selectedMode = $connectFourStore.mode;
</script>

<div>
	<button
		class="beginner"
		class:selected={selectedMode === 'beginner'}
		on:click={() => connectFourStore.update((cf) => ({ ...cf, mode: 'beginner' }))}>Beginner</button
	>
	<button
		class="intermediate"
		class:selected={selectedMode === 'intermediate'}
		on:click={() => connectFourStore.update((cf) => ({ ...cf, mode: 'intermediate' }))}
		>Intermediate</button
	>
	<button
		class="expert"
		class:selected={selectedMode === 'expert'}
		on:click={() => connectFourStore.update((cf) => ({ ...cf, mode: 'expert' }))}>Expert</button
	>
</div>

<style>
	div {
		display: flex;
		flex-direction: row;
		position: absolute;
		top: 10px;
		left: 10px;
		padding: 0.5rem 1rem;
	}

	.selected {
		background-color: darksalmon;
	}

	button {
		padding: 0.5rem;
		outline: none;
		border: none;
	}

	.beginner {
		border-radius: 5px 0 0 5px;
	}

	.intermediate {
		border-radius: 0;
		border: solid 1px;
		border-top: none;
		border-bottom: none;
	}

	.expert {
		border-radius: 0 5px 5px 0;
	}
</style>
