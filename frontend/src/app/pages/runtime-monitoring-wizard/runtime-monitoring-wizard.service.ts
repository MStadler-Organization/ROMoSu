import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {ConfigFileData, RTConfig, SumType} from "../../shared/models/interfaces";

@Injectable({
  providedIn: "root"
})
export class RuntimeMonitoringWizardService {

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
   * REST call to server to get the Sum types
   */
  getSumTypes(): Observable<SumType[]> {
    return this.http.get<SumType[]>(this.baseApiURL + "sum-types/");
  }


  /**
   * REST call to server to get the configs for a give sum type id
   */
  getConfigsForSuMType(pSuMTypeId: number): Observable<ConfigFileData[]> {
    return this.http.get<ConfigFileData[]>(this.baseApiURL + `config-file/?sum_type=${pSuMTypeId}`);
  }

  /**
   * REST call to server to post the runtime config
   */
  postRTStatus(pRTConfig: RTConfig): Observable<RTConfig> {
    return this.http.post<RTConfig>(this.baseApiURL + "runtime-config/", {pRTConfig});
  }
}
