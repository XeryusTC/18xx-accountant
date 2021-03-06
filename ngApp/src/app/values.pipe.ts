// Taken from https://webcake.co/object-properties-in-angular-2s-ngfor/
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
	name: 'values'
})
export class ValuesPipe implements PipeTransform {
	transform(value: any, sortBy: any, args?: any): any {
		if (value === undefined)
			return [];
		// create instance vars to store keys and final output
		let keyArr: any[] = Object.keys(value),
			dataArr = [];

		// loop through the object, pushing values to the return array
		keyArr.forEach((key: any) => {
			dataArr.push(value[key]);
		});

		if (sortBy) {
			dataArr.sort((a: Object, b: Object): number => {
				return a[sortBy] > b[sortBy] ? 1 : -1;
			});
		}

		// return the resulting array
		return dataArr;
	}
}
