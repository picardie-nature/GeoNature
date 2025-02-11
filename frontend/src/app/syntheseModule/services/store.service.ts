import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class SyntheseStoreService {
  public idSyntheseList: Array<number>;
  public data: {
    [key: string]: Array<any>
  } = {};
  constructor() {}
}
