export class Player {
	shares = [];

	constructor(
		public uuid: string,
		public game: string,
		public name: string,
		public cash: number
	) { }

	static fromJson(obj) {
		let player = new Player(obj.uuid, obj.game, obj.name, obj.cash);
		player.shares = obj.shares;
		return player;
	}
}
