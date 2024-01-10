<script>
	import ConnectFour from './ConnectFour.svelte';
</script>

<svelte:head>
	<title>Connect Four</title>
	<meta name="description" content="Play connect four with an AI" />
</svelte:head>

<section>
	<ConnectFour />
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

</style>
