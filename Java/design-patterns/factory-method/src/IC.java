public class IC implements Fahrzeug{
    public String beschreibung(){
        return "Der IC hält des Öfteren und erreicht auf den Strecken zwischen den Bahnhöfen eine Maximalgeschwindigkeit von 200km/h";
    }
    public double preisBerechnen(double distanz){
        return distanz * 1.5;
    }
}
