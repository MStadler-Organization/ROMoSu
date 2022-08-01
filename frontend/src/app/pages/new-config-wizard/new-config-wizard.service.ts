import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: "root"
})
export class NewConfigWizardService {

  private readonly baseApiURL: string;

  constructor(private readonly http: HttpClient) {
    this.baseApiURL = "http://127.0.0.1:8000/";
  }

  getSuMs(): Observable<string[]> {
    return this.http.get<string[]>(this.baseApiURL + "possible-sums/");
  }
}
