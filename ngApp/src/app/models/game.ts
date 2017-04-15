export class Game {
	companies = [];
	players = [];
	constructor(
		public uuid: string,
		public cash: number
	) { }

	static fromJson(obj) {
		return new Game(obj.uuid, obj.cash);
	}
}
