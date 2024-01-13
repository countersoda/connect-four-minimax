<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { connectFourStore } from '../store/ConnectFour';

	let hoveredColumn: number | undefined;

	function setHoveredColumn(column: number) {
		hoveredColumn = column;
	}

	function clearHoveredColumn() {
		hoveredColumn = undefined;
	}
	onMount(() => {
		connectFourStore.createConnectFour();
	});

	function render(value: number) {
		switch (value) {
			case 1:
				return 'red';
			case 2:
				return 'yellow';
			default:
				return 'transparent';
		}
	}

	async function handleClick(columnIndex: number) {
		await connectFourStore.makeTurn(columnIndex);
		await new Promise((r) => setTimeout(r, 500));
		connectFourStore.aiTurn();
	}

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
</script>

<svelte:head>
	<title>Connect Four</title>
	<meta name="description" content="A Connect Four game in SvelteKit" />
</svelte:head>

{#if $connectFourStore.gameover && $connectFourStore.winner === 1}
	<h1>You won!</h1>
{:else if $connectFourStore.gameover && $connectFourStore.winner === 2}
	<h1>Game Over</h1>
{/if}
<button class="restart" on:click={() => connectFourStore.createConnectFour()}>Restart</button>

{#if $connectFourStore.board}
	<div class="grid">
		{#each $connectFourStore.board as row, rowIndex}
			<div class="row" class:first={rowIndex === 5}>
				{#each row as _, columnIndex}
					<!-- svelte-ignore a11y-mouse-events-have-key-events -->
					<button
						class="letter"
						class:last={columnIndex === 6}
						class:hovered={columnIndex === hoveredColumn && !$connectFourStore.gameover}
						on:mouseover={() => setHoveredColumn(columnIndex)}
						on:mouseout={clearHoveredColumn}
						tabindex={1}
						on:click={() => handleClick(columnIndex)}
						disabled={$connectFourStore.gameover}
					>
						<span class:fall={$connectFourStore.board[rowIndex][columnIndex] !== 0}>
							<svg width="100" height="100">
								<circle
									cx="50"
									cy="50"
									r="30"
									stroke-width="3"
									stroke={$connectFourStore.board[rowIndex][columnIndex] === 0
										? 'transparent'
										: 'black'}
									fill={render($connectFourStore.board[rowIndex][columnIndex])}
								/>
							</svg>
						</span>
					</button>
				{/each}
			</div>
		{/each}
	</div>
{/if}

<style>
	.grid {
		--width: min(100vw, 40vh, 380px);
		max-width: var(--width);
		align-self: center;
		justify-self: center;
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
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

	.letter {
		border-top: none;
		border-bottom: none;
		border-right: none;
		border-left: solid;
		border-color: darksalmon;
		aspect-ratio: 1;
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		text-align: center;
		box-sizing: border-box;
		font-size: calc(0.08 * var(--width));
		background: white;
		margin: 0;
		color: rgba(0, 0, 0, 0.7);
		transition: background-color 0.3s;
	}

	.letter.last {
		border-right: solid;
		border-color: darksalmon;
	}

	.fall {
		animation: falling 600ms ease-in-out; /* Apply the 'falling' animation */
	}

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

	@keyframes falling {
		0% {
			transform: translateY(-500px); /* Start above */
			opacity: 0;
		}
		65% {
			transform: translateY(0); /* First contact with the ground */
			opacity: 1;
		}
		70% {
			transform: translateY(-50px); /* First bounce */
		}
		80% {
			transform: translateY(0); /* Return to ground */
		}
		90% {
			transform: translateY(-25px); /* Second bounce */
		}
		100% {
			transform: translateY(0); /* Settle down */
		}
	}
</style>
