import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ManageSumTypesComponent} from './manage-sum-types.component';

describe('ManageSumTypesComponent', () => {
  let component: ManageSumTypesComponent;
  let fixture: ComponentFixture<ManageSumTypesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ManageSumTypesComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ManageSumTypesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
