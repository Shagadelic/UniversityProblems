public class ICE implements Fahrzeug{
    public String beschreibung(){
        return "Der ICE erreicht auf den Strecken zwischen den Bahnhöfen eine Maximalgeschwindigkeit von 230 - 320 km/h";
    }
    public double preisBerechnen(double distanz){
        return distanz * 2;
    }
}
