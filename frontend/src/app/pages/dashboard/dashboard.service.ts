import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {ConfigFileData, RTConfig, SumType} from "../../shared/models/interfaces";

@Injectable({
  providedIn: "root"
})
export class DashboardService {

  private readonly baseApiURL: string;

  constructor(private readonly http: HttpClient) {
    this.baseApiURL = "http://127.0.0.1:8000/";
  }

  /**
   * REST call to server to get possible SuMs
   */
  getActiveRTConfigs(): Observable<RTConfig[]> {
    return this.http.get<RTConfig[]>(this.baseApiURL + "runtime-config/");
  }


  /**
   * REST call to server to get all configs
   */
  getAllConfigs(): Observable<ConfigFileData[]> {
    return this.http.get<ConfigFileData[]>(this.baseApiURL + "config-file/");
  }


  /**
   * REST call to server to get the Sum types
   */
  getSumTypes(): Observable<SumType[]> {
    return this.http.get<SumType[]>(this.baseApiURL + "sum-types/");
  }

  stopMonitoring(id: string): Observable<RTConfig> {
    return this.http.delete<RTConfig>(this.baseApiURL + `runtime-config/?id=${id}`);
  }
}
