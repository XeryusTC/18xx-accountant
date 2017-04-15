export class Game {
	companies = [];
	players = [];
	constructor(
		public uuid: string,
		public cash: number
	) { }

	static fromJson(obj) {
		let game = new Game(obj.uuid, obj.cash);
		game.companies = obj.companies;
		game.players = obj.players;
		return game;
	}
}
