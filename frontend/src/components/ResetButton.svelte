<script>
	import { connectFourStore } from '../store/ConnectFour';
</script>

<button class="restart" on:click={() => connectFourStore.createConnectFour()}>Restart</button>

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
