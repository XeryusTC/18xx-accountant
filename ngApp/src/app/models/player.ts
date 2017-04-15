export class Player {
	shares = [];

	constructor(
		public uuid: string,
		public game: string,
		public name: string,
		public cash: number
	) { }

	static fromJson(obj) {
		return new Player(obj.uuid, obj.game, obj.name, obj.cash);
	}
}
