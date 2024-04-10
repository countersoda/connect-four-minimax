<script lang="ts">
	import { connectFourStore } from '../store/ConnectFour';

	export let columnIndex: number;
	export let rowIndex: number;
	export let hoveredColumn: number | undefined;

	export let hoverColumn: () => void;
	export let mouseout: () => void;

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
</script>

<!-- svelte-ignore a11y-mouse-events-have-key-events -->
<button
	class="letter"
	class:last={columnIndex === 6}
	class:hovered={columnIndex === hoveredColumn && !$connectFourStore.gameover}
	on:mouseover={hoverColumn}
	on:mouseout={mouseout}
	tabindex={1}
	on:click={() => handleClick(columnIndex)}
	disabled={$connectFourStore.gameover}
>
	<span class:fall={$connectFourStore.board[rowIndex][columnIndex] !== 0}>
		<svg width="70" height="70">
			<circle
				cx="35"
				cy="35"
				r="30"
				stroke-width="3"
				stroke={$connectFourStore.board[rowIndex][columnIndex] === 0 ? 'transparent' : 'black'}
				fill={render($connectFourStore.board[rowIndex][columnIndex])}
			/>
		</svg>
	</span>
</button>

<style>
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
		animation: falling 400ms ease-in-out; /* Apply the 'falling' animation */
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
			transform: translateY(-30px); /* First bounce */
		}
		80% {
			transform: translateY(0); /* Return to ground */
		}
		90% {
			transform: translateY(-15px); /* Second bounce */
		}
		100% {
			transform: translateY(0); /* Settle down */
		}
	}
</style>
