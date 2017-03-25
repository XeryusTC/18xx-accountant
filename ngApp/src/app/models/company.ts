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
}
