# Frontend

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 14.0.4.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.io/cli) page.


# Custom Notes

Used Node JS Version: v16.15.1

### Code Generation

#### Generate new Angular UI Component
`ng generate @schematics/angular:component --name=shared/components/{component-name} --project=sudoku-frontend --module=shared`

This creates a new shared Component in shared/components and exports it via `SharedModule`

Replace `{component-name}` with the name of the component

#### Generate new Angular Page Component with Lazy loaded Routing
`ng generate @schematics/angular:module --name=/pages/{pagename} --project=sudoku-frontend --module=app --route={routename} --routing`

This creates a new Module as well as a Component in the /pages directory and Modifies `app.routing.module` to set up a lazy loaded route.

Replace `{pagename}` with the name of the component and `{routename}` with the name of the route in the URL

#### Create Backend Nest Feature Module
`ng generate @nrwl/nest:module --name=/{module} --project=sudoku-backend --language=ts`

Creates a new Module at `{modulename}`

#### Create Backend Nest Controller
`ng generate @nrwl/nest:controller --name=/{feature} --project=sudoku-backend --language=ts`

Creates a new Controller at `{feature}`
