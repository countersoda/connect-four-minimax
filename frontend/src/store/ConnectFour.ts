import { writable } from 'svelte/store';

export type DifficultyMode = 'beginner' | 'intermediate' | 'expert';

interface ConnectFour {
	id: string;
	board: number[][];
	turn: number;
	gameover: boolean;
	winner: number;
	mode: DifficultyMode;
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

const modeToDepth = (mode: DifficultyMode) => {
	switch (mode) {
		case 'beginner':
			return 2;
		case 'intermediate':
			return 3;
		case 'expert':
			return 4;
	}
};

const createConnectFourStore = () => {
	const { subscribe, update } = writable({ mode: 'beginner' } as ConnectFour);
	return {
		subscribe,
		update,
		createConnectFour: async (mode: DifficultyMode) => {
			const res = await fetch('http://127.0.0.1:5000/create_game', {
				method: 'post',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ depth: modeToDepth(mode) })
			});
			const data: CreateConnectFourResponse = await res.json();
			update((cf) => ({
				...cf,
				id: data.game_id,
				board: data.board,
				turn: 0,
				gameover: data.is_game_over,
				winner: -1
			}));
		},
		makeTurn: async (column: number) => {
			subscribe(async (connectFour) => {
				const res = await fetch(`http://127.0.0.1:5000/take_turn/${connectFour.id}`, {
					body: JSON.stringify({ column }),
					method: 'post',
					headers: { 'Content-Type': 'application/json' }
				});
				const data: TurnResponse = await res.json();
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
				const data: TurnResponse = await res.json();
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
