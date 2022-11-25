import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {RTConfig} from "../../shared/models/interfaces";

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
}
