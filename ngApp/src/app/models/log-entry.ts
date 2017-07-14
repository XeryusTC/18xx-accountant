export class LogEntry {
	constructor(
		public uuid: string,
		public game: string,
		public time: Date,
		public text: string,
	) { }

	static fromJson(obj) {
		let entry = new LogEntry(obj.uuid, obj.game, new Date(obj.time),
								 obj.text);
		return entry;
	}
}
