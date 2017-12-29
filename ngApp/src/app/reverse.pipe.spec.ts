import { ReversePipe } from './reverse.pipe';

describe('ReversePipe', () => {
	let pipe;
	let testArray;

	beforeEach(() => {
		pipe = new ReversePipe();
	});

	it('When the array is empty the result is empty', () => {
		testArray = [];
		expect(pipe.transform(testArray)).toEqual([]);
	});

	it('Returns reversed version of array', () => {
		testArray = [1, 2, 3, 4, 5];
		expect(pipe.transform(testArray)).toEqual([5, 4, 3, 2, 1]);
	});

	it('returns empty array when input undefined', () => {
		expect(pipe.transform(undefined)).toEqual([]);
	});
});
