export class Company {
	bank_shares: number;
	ipo_shares: number;
	value: number;
	share_set: string[];

	constructor(
		public uuid: string,
		public game: string,
		public name: string,
		public cash: number,
		public share_count: number,
		public text_color: string = "black",
		public background_color: string = "white"
	) {
		this.bank_shares = 0;
		this.ipo_shares = share_count;
		this.value = 0;
		this.share_set = [];
	}

	static fromJson(obj) {
	  let uuid = obj.uuid || obj._id_;
		let company = new Company(uuid, obj.game, obj.name, obj.cash,
								  obj.share_count, obj.text_color,
								  obj.background_color);
		company.bank_shares = obj.bank_shares;
		company.ipo_shares = obj.ipo_shares;
		company.share_set = obj.share_set;
		return company;
	}
}
