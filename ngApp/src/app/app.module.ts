import { BrowserModule, Title } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { StartPageComponent } from './start-page/start-page.component';
import { StartGameFormComponent } from
	'./start-game-form/start-game-form.component';

import { GameService } from './game.service';
import { PlayerService } from './player.service';

import { GameRoutingModule } from './game-routing.module';
import { GamePageComponent } from './game-page/game-page.component';
import { BankDetailComponent } from './bank-detail/bank-detail.component';
import { MenuComponent } from './menu/menu.component';
import { AddPlayerComponent } from './add-player/add-player.component';
import { AddPlayerFormComponent } from 
	'./add-player-form/add-player-form.component';

@NgModule({
	declarations: [
		AppComponent,
		StartGameFormComponent,
		StartPageComponent,
		GamePageComponent,
		BankDetailComponent,
		MenuComponent,
		AddPlayerComponent,
		AddPlayerFormComponent
	],
	imports: [
		BrowserModule,
		FormsModule,
		HttpModule,
		GameRoutingModule
	],
	providers: [
		GameService,
		PlayerService,
		Title
	],
	bootstrap: [AppComponent]
})
export class AppModule { }
