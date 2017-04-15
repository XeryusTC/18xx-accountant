export class Company {
	bank_shares: number;
	ipo_shares: number;
	constructor(
		public uuid: string,
		public game: string,
		public name: string,
		public cash: number,
		public share_count: number,
		public text_color: string = "black",
		public background_color: string = "white"
	) { }

	static fromJson(obj) {
		return new Company(obj.uuid, obj.game, obj.name, obj.cash,
						   obj.share_count, obj.text_color,
						   obj.background_color);
	}
}
