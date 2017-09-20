import { BrowserModule, Title } from '@angular/platform-browser';
import { NgModule }             from '@angular/core';
import { FormsModule }          from '@angular/forms';
import { HttpModule }           from '@angular/http';

import { ColorsService }        from './colors.service';
import { CompanyService }       from './company.service';
import { ErrorService }         from './error.service';
import { GameService }          from './game.service';
import { GameStateService }     from './game-state.service';
import { LogService }           from './log.service';
import { NetWorthService }      from './net-worth.service';
import { OperateService }       from './operate.service';
import { PlayerService }        from './player.service';
import { ShareService }         from './share.service';
import { TransferMoneyService } from './transfer-money.service';
import { TransferShareService } from './transfer-share.service';
import { UndoService }          from './undo.service';

import { ValuesPipe } from './values.pipe';

import { AddCompanyComponent }  from './add-company/add-company.component';
import { AddCompanyFormComponent }
	from './add-company-form/add-company-form.component';
import { AddPlayerComponent }   from './add-player/add-player.component';
import { AddPlayerFormComponent }
	from './add-player-form/add-player-form.component';
import { AppComponent }         from './app.component';
import { BankDetailComponent }  from './bank-detail/bank-detail.component';
import { CompanySectionComponent }
	from './company-section/company-section.component';
import { GamePageComponent }    from './game-page/game-page.component';
import { GameRoutingModule }    from './game-routing.module';
import { MenuComponent }        from './menu/menu.component';
import { OperateFormComponent } from './operate-form/operate-form.component';
import { PlayerSectionComponent }
	from './player-section/player-section.component';
import { ShareFormComponent }   from './share-form/share-form.component';
import { StartGameFormComponent }
	from './start-game-form/start-game-form.component';
import { StartPageComponent }   from './start-page/start-page.component';
import { TransferFormComponent }
	from './transfer-form/transfer-form.component';
import { ErrorDisplayComponent } from './error-display/error-display.component';
import { LogSectionComponent } from './log-section/log-section.component';
import { SettingsSectionComponent } from './settings-section/settings-section.component';
import { NetWorthComponent } from './net-worth/net-worth.component';
import { EditCompanyComponent } from './edit-company/edit-company.component';
import { EditCompanyFormComponent } from './edit-company-form/edit-company-form.component';

@NgModule({
	declarations: [
		AddCompanyComponent,
		AddCompanyFormComponent,
		AddPlayerComponent,
		AddPlayerFormComponent,
		AppComponent,
		BankDetailComponent,
		CompanySectionComponent,
		GamePageComponent,
		MenuComponent,
		OperateFormComponent,
		PlayerSectionComponent,
		ShareFormComponent,
		StartGameFormComponent,
		StartPageComponent,
		TransferFormComponent,
		ValuesPipe,
		ErrorDisplayComponent,
		LogSectionComponent,
		SettingsSectionComponent,
		NetWorthComponent,
		EditCompanyComponent,
		EditCompanyFormComponent,
	],
	imports: [
		BrowserModule,
		FormsModule,
		HttpModule,
		GameRoutingModule
	],
	providers: [
		ColorsService,
		CompanyService,
		ErrorService,
		GameStateService,
		GameService,
		LogService,
		NetWorthService,
		OperateService,
		PlayerService,
		ShareService,
		Title,
		TransferMoneyService,
		TransferShareService,
		UndoService
	],
	bootstrap: [AppComponent]
})
export class AppModule { }
