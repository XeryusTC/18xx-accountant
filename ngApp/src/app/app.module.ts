import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { StartPageComponent } from './start-page/start-page.component';
import { StartGameFormComponent } from
	'./start-game-form/start-game-form.component';

import { GameService } from './game.service';

import { GameRoutingModule } from './game-routing.module';
import { GamePageComponent } from './game-page/game-page.component';
import { BankDetailComponent } from './bank-detail/bank-detail.component';

@NgModule({
	declarations: [
		AppComponent,
		StartGameFormComponent,
		StartPageComponent,
		GamePageComponent,
		BankDetailComponent
	],
	imports: [
		BrowserModule,
		FormsModule,
		HttpModule,
		GameRoutingModule
	],
	providers: [
		GameService
	],
	bootstrap: [AppComponent]
})
export class AppModule { }
