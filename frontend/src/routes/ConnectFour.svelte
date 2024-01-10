<script lang="ts">
	import { onMount } from "svelte";
	import { connectFourStore } from "../store/game";

    let hoveredColumn: number | undefined;

    function setHoveredColumn(column:number) {
        hoveredColumn = column;
    }

    function clearHoveredColumn() {
        hoveredColumn = undefined;
    }
	onMount(() => {
		connectFourStore.createConnectFour()
	})

	function render(value: number){
		switch(value){
			case 1:
				return "X"
			case 2:
				return "O"
			default:
				return " "
		}
	}

	function handleClick(columnIndex:number) {
		connectFourStore.makeTurn(columnIndex).then(() => setTimeout(() => connectFourStore.aiTurn(), 500))
	}
</script>

<svelte:head>
	<title>Connect Four</title>
	<meta name="description" content="A Connect Four game in SvelteKit" />
</svelte:head>

{#if $connectFourStore.board}
<div class="grid">
	{#each $connectFourStore.board as row,rowIndex}
	<div class="row" class:first={rowIndex === 5}>
		{#each row as column, columnIndex}
            <!-- svelte-ignore a11y-mouse-events-have-key-events -->
            <button
                class="letter" 
                class:last={columnIndex===6} 
                class:hovered={columnIndex === hoveredColumn}
                on:mouseover={() => setHoveredColumn(columnIndex)}
                on:mouseout={clearHoveredColumn} tabindex={1}
				on:click={() => handleClick(columnIndex)}
				>
				{render($connectFourStore.board[rowIndex][columnIndex])}
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
		border-right:none;
        border-left:solid;
        border-color: darksalmon;
		aspect-ratio: 1;
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		text-align: center;
		box-sizing: border-box;
		text-transform: lowercase;
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

	@keyframes wiggle {
		0% {
			transform: translateX(0);
		}
		10% {
			transform: translateX(-2px);
		}
		30% {
			transform: translateX(4px);
		}
		50% {
			transform: translateX(-6px);
		}
		70% {
			transform: translateX(+4px);
		}
		90% {
			transform: translateX(-2px);
		}
		100% {
			transform: translateX(0);
		}
	}
</style>
