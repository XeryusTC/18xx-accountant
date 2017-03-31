import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA }                 from '@angular/core';

import { ActivatedRoute, ActivatedRouteStub } from '../testing/router-stubs';
import { GamePageComponent } from './game-page.component';
import { GameService } from '../game.service';
import { PlayerService } from '../player.service';
import { CompanyService } from '../company.service';

describe('GamePageComponent', () => {
	let component: GamePageComponent;
	let fixture: ComponentFixture<GamePageComponent>;
	let activatedRoute: ActivatedRouteStub;
	let gameServiceStub = {
		getGame: (() => {
			return new Promise((resolve, reject) => {});
		})
	}
	let playerServiceStub = {
		getPlayer: true
	}
	let companyServiceStub = {
		getCompany: true
	}

	beforeEach(async(() => {
		activatedRoute = new ActivatedRouteStub();
		TestBed.configureTestingModule({
			declarations: [GamePageComponent],
			schemas: [NO_ERRORS_SCHEMA],
			providers: [
				{provide: ActivatedRoute, useValue: activatedRoute},
				{provide: GameService, useValue: gameServiceStub},
				{provide: PlayerService, useValue: playerServiceStub},
				{provide: CompanyService, useValue: companyServiceStub}
			]
		})
		.compileComponents();
	}));

	beforeEach(() => {
		activatedRoute.testParams = {uuid: 'test'};
		fixture = TestBed.createComponent(GamePageComponent);
		component = fixture.componentInstance;
		fixture.detectChanges();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
