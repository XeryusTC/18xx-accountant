import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { StartPageComponent } from './start-page/start-page.component';
import { GamePageComponent }  from './game-page/game-page.component';
import { AddPlayerComponent } from './add-player/add-player.component';
import { AddCompanyComponent } from './add-company/add-company.component';

const routes: Routes = [
	{path: '', component: StartPageComponent},
	{path: 'game/:uuid', component: GamePageComponent},
	{path: 'game/:uuid/add-player', component: AddPlayerComponent},
	{path: 'game/:uuid/add-company', component: AddCompanyComponent}
];

@NgModule({
	imports: [ RouterModule.forRoot(routes) ],
	exports: [ RouterModule ]
})
export class GameRoutingModule {}
