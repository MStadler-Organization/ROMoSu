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

  /**
   * REST call to server to get possible SuMs
   */
  getSuMs(): Observable<string[]> {
    return this.http.get<string[]>(this.baseApiURL + "possible-sums/");
  }

  /**
   * REST call to server to get topics associated with a selected SuM
   * @param pSum the name of the SuM as string
   */
  getPropsForSum(pSum: string): Observable<any> {
    return this.http.get<any>(this.baseApiURL + `props-for-sum/?sum=${pSum}`);
  }
}
