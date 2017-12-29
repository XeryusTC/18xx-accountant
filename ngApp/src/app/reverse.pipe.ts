// Taken from https://stackoverflow.com/questions/35703258/
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
	name: 'reverse',
	pure: false
})
export class ReversePipe implements PipeTransform {
	transform(value) {
		if (value === undefined)
			return [];
		return value.slice().reverse();
	}
}
