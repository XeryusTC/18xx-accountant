export class Game {
	companies = [];
	players = [];
	constructor(
		public uuid: string,
		public cash: number,
		public pool_shares_pay: boolean = false,
		public ipo_shares_pay: boolean = false,
		public treasury_shares_pay: boolean = true
	) { }

	static fromJson(obj) {
		let game = new Game(obj.uuid, obj.cash, obj.pool_shares_pay,
						    obj.ipo_shares_pay, obj.treasury_shares_pay);
		game.companies = obj.companies;
		game.players = obj.players;
		return game;
	}
}
