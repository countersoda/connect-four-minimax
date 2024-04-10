<script>
	import { connectFourStore } from '../store/ConnectFour';
</script>

{#if $connectFourStore.gameover && $connectFourStore.winner === 1}
	<h1>You won!</h1>
{:else if $connectFourStore.gameover && $connectFourStore.winner === 2}
	<h1>Game Over</h1>
{:else}
	<h1>Play</h1>
{/if}
