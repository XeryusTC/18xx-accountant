export class LogEntry {
	constructor(
		public uuid: string,
		public game: string,
		public time: Date,
		public text: string,
		public acting_company: string = null,
		public is_undoable: boolean = false,
	) { }

	static fromJson(obj) {
		let entry = new LogEntry(obj.uuid, obj.game, new Date(obj.time),
								 obj.text, obj.acting_company,
								 obj.is_undoable);
		return entry;
	}
}
