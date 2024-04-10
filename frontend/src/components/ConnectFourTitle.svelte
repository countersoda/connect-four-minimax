<script>
	import { connectFourStore } from '../store/ConnectFour';
	import Confetti from 'svelte-confetti';
</script>

{#if $connectFourStore.gameover && $connectFourStore.winner === 1}
	<div>
		<Confetti
			x={[-5, 5]}
			y={[0, 0.1]}
			delay={[500, 2000]}
			infinite
			duration={5000}
			amount={500}
			fallDistance="100vh"
		/>
		<section>
			<h1>You won!</h1>
			<p>Press R to restart</p>
		</section>
	</div>
{:else if $connectFourStore.gameover && $connectFourStore.winner === 2}
	<div>
		<h1>Game Over</h1>
		<p>Press R to restart</p>
	</div>
{/if}

<style>
	div {
		width: 100%;
		height: 100%;
		position: absolute;
		background-color: rgba(0, 0, 0, 0.8);
		color: white;
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	section {
		display: flex;
		flex-direction: column;
		height: 100%;
		justify-content: center;
		align-items: center;
	}
</style>
