import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrendingByTimeComponent } from './trending-by-time.component';

describe('TrendingByTimeComponent', () => {
  let component: TrendingByTimeComponent;
  let fixture: ComponentFixture<TrendingByTimeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrendingByTimeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrendingByTimeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
