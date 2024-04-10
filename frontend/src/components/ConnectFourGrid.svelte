<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { connectFourStore } from '../store/ConnectFour';
	import ConnectFourToken from './ConnectFourToken.svelte';

	let hoveredColumn: number | undefined;

	onMount(() => {
		connectFourStore.createConnectFour();
	});

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'r' || event.key === 'R') {
			connectFourStore.createConnectFour();
		}
	}

	onMount(() => {
		if (typeof window !== 'undefined') window.addEventListener('keydown', handleKeyPress);
	});

	onDestroy(() => {
		if (typeof window !== 'undefined') window.removeEventListener('keydown', handleKeyPress);
	});

	function setHoveredColumn(column: number) {
		hoveredColumn = column;
	}

	function clearHoveredColumn() {
		hoveredColumn = undefined;
	}
</script>

<svelte:head>
	<title>Connect Four</title>
	<meta name="description" content="A Connect Four game in SvelteKit" />
</svelte:head>

{#if $connectFourStore.gameover && $connectFourStore.winner === 1}
	<h1>You won!</h1>
{:else if $connectFourStore.gameover && $connectFourStore.winner === 2}
	<h1>Game Over</h1>
{:else}
	<h1>Play</h1>
{/if}

{#if $connectFourStore.board}
	<div class="grid">
		{#each $connectFourStore.board as row, rowIndex}
			<div class="row" class:first={rowIndex === 5}>
				{#each row as _, columnIndex}
					<!-- svelte-ignore a11y-mouse-events-have-key-events -->
					<ConnectFourToken
						{rowIndex}
						{columnIndex}
						{hoveredColumn}
						mouseout={clearHoveredColumn}
						hoverColumn={() => setHoveredColumn(columnIndex)}
					/>
				{/each}
			</div>
		{/each}
	</div>
{/if}

<style>
	.grid {
		justify-self: center;
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
		cursor: pointer;
	}

	.grid .row {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
	}

	.row.first {
		border-bottom: solid;
		border-color: darksalmon;
	}

	:global(.grid .row .letter.hovered) {
		background-color: antiquewhite;
	}
</style>
