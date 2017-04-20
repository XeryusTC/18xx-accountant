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

	it('returns array sorted when given key to sort by', () => {
		testDict = {
			first:  {name: 'Alice', other: 'longish-value'},
			second: {name: 'Charlie', other: 'other-value'},
			third:  {name: 'Bob', other: 'different-value'},
		};
		expect(pipe.transform(testDict, 'name')).toEqual([
			{name: 'Alice', other: 'longish-value'},
			{name: 'Bob', other: 'different-value'},
			{name: 'Charlie', other: 'other-value'}
		]);
		expect(pipe.transform(testDict, 'other')).toEqual([
			{name: 'Bob', other: 'different-value'},
			{name: 'Alice', other: 'longish-value'},
			{name: 'Charlie', other: 'other-value'}
		]);
	});
});
