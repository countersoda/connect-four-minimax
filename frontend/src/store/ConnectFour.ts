import { writable } from 'svelte/store';

interface ConnectFour {
	id: string;
	board: number[][];
	turn: number;
	gameover: boolean;
	winner: number;
}

interface CreateConnectFourResponse {
	game_id: string;
	board: number[][];
	is_game_over: boolean;
}

interface TurnResponse {
	status: boolean;
	board: number[][];
	is_game_over: boolean;
	winner: number;
}

const createConnectFourStore = () => {
	const { subscribe, set, update } = writable({} as ConnectFour);
	return {
		subscribe,
		createConnectFour: async () => {
			const res = await fetch('http://127.0.0.1:5000/create_game', { method: 'post' });
			const data = (await res.json()) as CreateConnectFourResponse;
			set({
				id: data.game_id,
				board: data.board,
				turn: 0,
				gameover: data.is_game_over,
				winner: -1
			});
		},
		makeTurn: async (column: number) => {
			subscribe(async (connectFour) => {
				const res = await fetch(`http://127.0.0.1:5000/take_turn/${connectFour.id}`, {
					body: JSON.stringify({ column }),
					method: 'post',
					headers: { 'Content-Type': 'application/json' }
				});
				const data = (await res.json()) as TurnResponse;
				if (data.status)
					update((cf) => ({
						...cf,
						board: data.board,
						gameover: data.is_game_over,
						winner: data.winner
					}));
			})();
		},
		aiTurn: async () => {
			subscribe(async (connectFour) => {
				const res = await fetch(`http://127.0.0.1:5000/check_ai_move/${connectFour.id}`, {});
				const data = (await res.json()) as TurnResponse;
				update((cf) => ({
					...cf,
					board: data.board,
					gameover: data.status ? data.is_game_over! : cf.gameover,
					winner: data.winner
				}));
			})();
		}
	};
};

export const connectFourStore = createConnectFourStore();
