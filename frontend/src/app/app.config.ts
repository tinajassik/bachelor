import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { withComponentInputBinding } from '@angular/router'; 

export const appConfig: ApplicationConfig = {
  providers: [provideRouter(routes, withComponentInputBinding())]  
};
