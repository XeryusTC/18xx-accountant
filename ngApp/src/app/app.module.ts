import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { StartPageComponent } from './start-page/start-page.component';
import { StartGameFormComponent } from
	'./start-game-form/start-game-form.component';

import { GameService } from './game.service';

@NgModule({
	declarations: [
		AppComponent,
		StartGameFormComponent,
		StartPageComponent
	],
	imports: [
		BrowserModule,
		FormsModule,
		HttpModule
	],
	providers: [
		GameService
	],
	bootstrap: [AppComponent]
})
export class AppModule { }
