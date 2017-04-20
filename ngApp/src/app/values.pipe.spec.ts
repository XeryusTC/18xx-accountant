import { ValuesPipe } from './values.pipe';

describe('ValuesPipe', () => {
	let pipe;
	let testDict;

	beforeEach(() => {
		pipe = new ValuesPipe();
	});

	it('When dictionary is empty result is empty', () => {
		testDict = {};
		expect(pipe.transform(testDict)).toEqual([]);
	});

	it('Converts dictionary to values only', () => {
		testDict = {
			key1: 1,
			key2: 2,
			key3: 3
		};
		expect(pipe.transform(testDict)).toEqual([1, 2, 3]);
	});

	it('returns empty array when input undefined', () => {
		expect(pipe.transform(undefined)).toEqual([]);
	});
});
