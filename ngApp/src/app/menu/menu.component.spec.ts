import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule }              from '@angular/router/testing';

import { MenuComponent } from './menu.component';
import { RouterLinkStubDirective } from '../testing/router-stubs';

describe('MenuComponent', () => {
	let component: MenuComponent;
	let fixture: ComponentFixture<MenuComponent>;

	beforeEach(async(() => {
		TestBed.configureTestingModule({
			imports: [RouterTestingModule],
			declarations: [ MenuComponent, RouterLinkStubDirective ]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		fixture = TestBed.createComponent(MenuComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
