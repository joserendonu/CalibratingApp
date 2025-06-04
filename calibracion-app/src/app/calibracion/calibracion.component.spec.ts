import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CalibracionComponent } from './calibracion.component';

describe('CalibracionComponent', () => {
  let component: CalibracionComponent;
  let fixture: ComponentFixture<CalibracionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CalibracionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CalibracionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
